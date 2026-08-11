# View Structure Examples

Use this reference when a Flutter view has ambiguous control boundaries or a deeply nested layout.
Adapt names, state binding, and directories to the target repository; preserve its established
architecture unless the task explicitly changes it.

## Contents

- Four levels and dependency direction
- Suggested feature layout
- Refactor a nested page
- Build a page-private skeleton
- Build a business control
- Build a business-independent control
- Choose a collection pattern
- Resolve ambiguous controls
- Detect under- and over-extraction
- Validate the result

## Four levels and dependency direction

Build abstractions upward:

```text
原生或第三方控件 -> 业务无关控件 -> 业务控件 -> 页面
```

| Level | Owns | May know | Must not know |
|---|---|---|---|
| Native/third-party | Rendering, layout, input, package capability | Its own configuration | Project features or business actions |
| Business-independent | Reusable project UI behavior | Generic values, children, builders, visual callbacks | Feature state, domain entities, routes, business decisions |
| Business | One named feature region | Typed view data and business callbacks | Page controller, route navigation, unrelated regions |
| Page | Screen composition and event routing | Existing state/logic binding and all business regions | Detailed primitive layout inside each region |

Read dependencies downward: a page may import feature business controls; a business control may
import shared UI controls; shared UI may import Flutter or packages. Do not reverse that direction.

A page-private shell remains at page level even when it accepts generic `Widget` children. Generic
types, statelessness, or reuse within one page do not make a control business-independent.

## Suggested feature layout

Use repository conventions first. When none exist, this layout keeps ownership visible:

```text
lib/
├── shared/ui/
│   └── pointer_scroll_view.dart       # business-independent
└── features/audio_home/
    ├── view.dart                      # page composition root
    ├── logic.dart                     # existing state/logic mechanism
    ├── state.dart                     # existing state/view data
    └── widget/
        ├── audio_home_function.dart   # page-private skeleton
        ├── side_navigation.dart       # business control
        ├── recommendation_section.dart
        ├── ranking_section.dart
        └── playback_console.dart
```

Do not create `logic.dart` or `state.dart` solely to match this tree. The skill governs view
composition, not state-management selection.

## Refactor a nested page

The problem is not nesting itself; the problem is that business structure and interaction entrances
are buried inside primitive layout details.

Before, the page owns every detail:

```dart
return Scaffold(
  body: Column(children: [
    Expanded(
      child: Row(children: [
        Container(child: Column(children: navigationItems.map(/* ... */).toList())),
        Expanded(
          child: Column(children: [
            Row(children: [/* search, refresh, settings ... */]),
            Expanded(
              child: SingleChildScrollView(
                child: Column(children: [/* banner, recommendations, ranking ... */]),
              ),
            ),
          ]),
        ),
      ]),
    ),
    Container(child: Row(children: [/* playback controls ... */])),
  ]),
);
```

After, keep region order, data, and callbacks visible:

```dart
class AudioHomePage extends StatelessWidget {
  const AudioHomePage({
    super.key,
    required this.data,
    required this.onNavigationTap,
    required this.onSearchChanged,
    required this.onRefresh,
    required this.onRecommendationTap,
    required this.onRankingTap,
    required this.onPlay,
  });

  final AudioHomeViewData data;
  final ValueChanged<NavigationItemViewData> onNavigationTap;
  final ValueChanged<String> onSearchChanged;
  final VoidCallback onRefresh;
  final ValueChanged<RecommendationItemViewData> onRecommendationTap;
  final ValueChanged<RankingItemViewData> onRankingTap;
  final VoidCallback onPlay;

  @override
  Widget build(BuildContext context) {
    return buildAudioHomePageShell(
      top: buildAudioHomeTopShell(
        navigation: SideNavigation(
          data: data.navigation,
          onItemTap: onNavigationTap,
        ),
        content: buildAudioHomeContentShell(
          header: AccountTools(
            data: data.accountTools,
            onSearchChanged: onSearchChanged,
            onRefresh: onRefresh,
          ),
          sections: [
            RecommendationSection(
              data: data.recommendations,
              onRefresh: onRefresh,
              onItemTap: onRecommendationTap,
            ),
            RankingSection(data: data.rankings, onItemTap: onRankingTap),
          ],
        ),
      ),
      bottom: PlaybackConsole(data: data.playback, onPlay: onPlay),
    );
  }
}
```

Bind `data` and callbacks with the repository's existing Provider, BLoC, GetX, Riverpod, signals, or
constructor-injection mechanism. Do not hide the page's major events inside the child controls.

## Build a page-private skeleton

Put stable screen geometry in `widget/audio_home_function.dart`. Use named slots when positions have
fixed meaning; use `children` when visible order is the useful abstraction.

```dart
Widget buildAudioHomePageShell({
  required Widget top,
  required Widget bottom,
}) {
  return Scaffold(body: Column(children: [Expanded(child: top), bottom]));
}

Widget buildAudioHomeTopShell({
  required Widget navigation,
  required Widget content,
}) {
  return Row(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [navigation, Expanded(child: content)],
  );
}

Widget buildAudioHomeContentShell({
  required Widget header,
  required List<Widget> sections,
}) {
  return Column(children: [
    header,
    Expanded(
      child: PointerScrollView(
        child: Column(children: sections),
      ),
    ),
  ]);
}
```

This skeleton is page-private because its top/bottom split, navigation slot, and scrolling region
encode one screen's geometry. Do not place it under `shared/ui/`.

## Build a business control

Give the control a typed view contract. Keep business actions as callbacks and primitive details
private. The example uses eager construction only because recommendations are small and bounded.

```dart
class RecommendationSection extends StatelessWidget {
  const RecommendationSection({
    super.key,
    required this.data,
    required this.onRefresh,
    required this.onItemTap,
  });

  final List<RecommendationItemViewData> data;
  final VoidCallback onRefresh;
  final ValueChanged<RecommendationItemViewData> onItemTap;

  @override
  Widget build(BuildContext context) {
    return _buildBackground(children: [
      _buildHeader(),
      _buildItems(itemBuilder: (item) => Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildCover(item),
          _buildTitle(item),
          _buildSubtitle(item),
        ],
      )),
    ]);
  }

  Widget _buildHeader() => Row(children: [
    const Expanded(child: Text('Recommended')),
    TextButton(onPressed: onRefresh, child: const Text('Refresh')),
  ]);

  Widget _buildItems({
    required Widget Function(RecommendationItemViewData item) itemBuilder,
  }) {
    return Wrap(
      spacing: 16,
      runSpacing: 16,
      children: data.map(itemBuilder).toList(growable: false),
    );
  }

  Widget _buildCover(RecommendationItemViewData item) => InkWell(
    onTap: () => onItemTap(item),
    child: Image.network(item.coverUrl, width: 150, height: 150, fit: BoxFit.cover),
  );

  Widget _buildTitle(RecommendationItemViewData item) => Text(item.title);
  Widget _buildSubtitle(RecommendationItemViewData item) => Text(item.subtitle);

  Widget _buildBackground({required List<Widget> children}) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 24),
    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: children),
  );
}
```

Do not replace a coherent typed view model with a map or an untyped bag. Do not make the control call
a page controller, navigator, repository, or datasource directly.

## Build a business-independent control

Keep a shared control free of feature types and actions. This wrapper adds mouse and touch drag
support without knowing why the content scrolls.

```dart
import 'dart:ui' show PointerDeviceKind;
import 'package:flutter/material.dart';

class PointerScrollView extends StatelessWidget {
  const PointerScrollView({super.key, required this.child, this.controller});

  final Widget child;
  final ScrollController? controller;

  @override
  Widget build(BuildContext context) {
    return ScrollConfiguration(
      behavior: const _PointerScrollBehavior(),
      child: SingleChildScrollView(controller: controller, child: child),
    );
  }
}

class _PointerScrollBehavior extends MaterialScrollBehavior {
  const _PointerScrollBehavior();

  @override
  Set<PointerDeviceKind> get dragDevices => const {
    PointerDeviceKind.touch,
    PointerDeviceKind.mouse,
  };
}
```

Accept an externally owned `ScrollController`; do not create a controller during every `build`.

## Choose a collection pattern

Choose from data size and scrolling semantics, not from a desire to make every list look alike.

### Small, fixed collection

Use eager `map` or `List.generate` when the upper bound is small and the parent must size all items,
such as a navigation menu or six recommendation cards. Keep the per-item shape in `itemBuilder`.

### Large, dynamic, or paginated collection

Preserve lazy construction and keys:

```dart
ListView.builder(
  itemCount: data.length,
  itemBuilder: (context, index) {
    final item = data[index];
    return RecommendationTile(
      key: ValueKey(item.id),
      data: item,
      onTap: () => onItemTap(item),
    );
  },
)
```

### Small nested collection

Use `itemBuilder + subBuilder` when both business levels matter and each group is bounded:

```dart
Widget buildNavigationGroups({
  required List<NavigationGroupViewData> groups,
  required List<Widget> Function(NavigationGroupViewData group) itemBuilder,
  required Widget Function(NavigationItemViewData item) subBuilder,
}) {
  return Column(
    children: groups.map((group) => Column(children: [
      ...itemBuilder(group),
      ...group.items.map(subBuilder),
    ])).toList(growable: false),
  );
}
```

Keep the call site business-readable:

```dart
buildNavigationGroups(
  groups: data,
  itemBuilder: (group) => [
    _buildGroupTitle(group.title),
  ],
  subBuilder: (item) => InkWell(
    onTap: () => onItemTap(item),
    child: Row(children: [
      _buildSelectionMarker(item),
      _buildItemIcon(item),
      _buildItemLabel(item),
    ]),
  ),
);
```

For large nested data, flatten groups into typed display rows or use slivers. Do not put an unbounded
`ListView` inside another scrollable merely to preserve the two-builder naming pattern.

## Resolve ambiguous controls

| Candidate | Usually belongs to | Reason or deciding question |
|---|---|---|
| Package carousel | Native/third-party | It supplies motion and paging capability only |
| Project carousel wrapper | Business-independent | It standardizes generic paging, indicators, or autoplay |
| Promotion banner | Business | It receives campaign data and emits promotion selection |
| Generic search field | Business-independent | It accepts text, decoration, and `onChanged` only |
| Catalog search bar | Business | It owns catalog-specific filters, suggestions, or actions |
| Image card shell | Business-independent | It renders generic image/title/child slots |
| Recommendation card | Business | It receives recommendation view data and emits item selection |
| Playback console | Business | Its controls and callbacks express audio-domain actions |
| Audio-home top split | Page-private | Its geometry belongs to one screen even if stateless |
| Loading or empty view | Business-independent if generic | Keep feature-specific retry meaning and copy in the business owner |
| Theme-aware button | Business-independent | Theme awareness is presentation, not business knowledge |
| Analytics navigation wrapper | Usually page/business owner | Emit the tap; keep analytics and navigation decisions outside generic UI |

Reuse count is evidence, not the definition. A control used once can still be business-independent;
a helper used three times inside one page can remain page-private.

## Detect under- and over-extraction

Under-extracted:

- The page contains decoration, item traversal, and gesture details for multiple regions.
- A maintainer must count nested `Row` and `Column` blocks to identify the screen.
- Business interactions are only discoverable by searching inside leaf Widgets.

Over-extracted:

- `_TitleText`, `_LeftPadding`, or `_CardRow` gets a separate file without an independent contract.
- A wrapper changes only a `Container` name and does not clarify ownership or hide stable detail.
- One business region is scattered across many files that cannot be understood independently.

Prefer a private `_buildXxx` method first. Promote it only when the child gains a stable contract,
independent meaning, meaningful reuse, or separate maintenance ownership.

## Validate the result

- Read the page top to bottom and name every major visible region without opening another file.
- Locate each region's data input and business callbacks from the page.
- Confirm shared UI imports no feature state, domain entity, route, repository, or page controller.
- Confirm business controls do not perform navigation or business orchestration internally.
- Confirm page-private geometry has not leaked into shared UI.
- Confirm lazy/eager construction, scrolling, keys, rebuild scope, and accessibility are preserved.
- Confirm a local visual change can be made inside one region without editing unrelated regions.

## Provenance

The patterns were distilled from
[Flutter 改善套娃地狱问题（仿喜马拉雅PC页面举例）](https://www.cnblogs.com/xdd666/p/14537818.html)
and the corresponding
[Flutter example](https://github.com/xdd666t/flutter_use/tree/master/lib/module/function/himalaya).
