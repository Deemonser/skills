---
name: flutter-no-nesting
description: 用于编写、重构或评审 Flutter 页面结构，尤其当页面出现“嵌套过深”“套娃”“widget tree 过长”“页面难维护”时使用。适用于把复杂页面重构为“view 组合 + function 骨架 + 业务 widget + builder 列表”的结构。默认采用统一命名的轻量目录：`logic.dart + state.dart + view.dart + widget/`；页面进入事件流模式时，再增加 `event.dart`。
version: 4.0.0
---

# Flutter No Nesting

这个 skill 基于《Flutter 改善套娃地狱问题（仿喜马拉雅PC页面举例）》的方法论。

目标不是机械减少 Widget 层级，而是把页面改造成：

- 结构一眼可读
- 事件入口集中
- 局部修改成本低
- 页面复杂但不失控

核心思想：

- `view.dart` 只负责组合业务区块和暴露事件入口
- `widget/[module]_function.dart` 吃掉稳定布局骨架
- 每个业务区块拆成有业务语义的 Widget
- 列表区块用 `itemBuilder / subBuilder` 组织，而不是把循环细节堆在主结构里

## 什么时候用

- 页面 `build` 超过一屏，读代码要靠数括号
- 页面同时混着布局细节、业务区块、事件回调、列表循环
- 后续会频繁改样式、改交互、插区块，但当前结构很难下手
- 页面已经有状态管理框架，但 view 层仍然是一大坨
- 用户明确提到“去嵌套”“套娃地狱”“页面结构优化”“按业务模块拆 Widget”

## 目录结构

这份 skill 只约束 view 组织方式，不强绑具体状态管理实现。默认统一采用：

```text
module_name/
├── logic.dart
├── state.dart
├── view.dart
└── widget/
    ├── module_name_function.dart
    ├── module_name_section_a.dart
    └── ...
```

如果页面进入明确的事件流模式，再增加：

```text
module_name/
├── event.dart
```

对应关系：

- `view.dart`：主页面，只做组合和事件转发
- `logic.dart`：统一的逻辑层坑位
- `state.dart`：页面数据源或页面状态
- `event.dart`：仅事件流模式存在
- `widget/module_name_function.dart`：稳定骨架函数
- `widget/*.dart`：具体业务区块

说明：

- 不用 `flutter_bloc` 时，`logic.dart` 可以是轻逻辑层
- 用 `flutter_bloc` 但只是页面状态时，`logic.dart` 通常实现为 `Cubit`
- 用 `flutter_bloc` 且是事件流时，`logic.dart` 通常实现为 `Bloc`，并额外增加 `event.dart`

## 先判断拆分层级

### 1. View 层

放这里的内容只有：

- 页面大区块的组合顺序
- 页面级状态读取
- 事件入口转发到 `logic`

不要放：

- 大段 `Container / Padding / Row / Column / Expanded`
- 列表遍历细节
- 某个业务卡片的样式实现

### 2. Function 骨架层

适合放进 `widget/[module]_function.dart` 的内容：

- 页面最外层 `Scaffold`
- 主 `Row / Column`
- 左右布局骨架
- 顶部 / 底部 / 滚动区外壳

特征：

- 结构稳定
- 业务含义弱
- 写完后改动频率低

```dart
Widget buildPageBg({required List<Widget> children}) {
  return Scaffold(
    backgroundColor: Colors.white,
    body: Column(children: children),
  );
}

Widget buildTopArea({required List<Widget> children}) {
  return Expanded(
    child: Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: children,
    ),
  );
}

Widget buildScrollableContent({required List<Widget> children}) {
  return Expanded(
    child: SingleChildScrollView(
      child: Column(children: children),
    ),
  );
}
```

### 3. 业务 Widget 层

适合拆成独立业务 Widget 的内容：

- 搜索区
- banner 区
- 猜你喜欢
- 榜单区
- 底部控制栏

名字应该体现业务语义，而不是 `_buildContainer2` 这种纯结构语义。

### 4. Widget 内部私有方法层

业务 Widget 内部的 `children`，优先继续拆成 `_buildXxx()` 方法，而不是一上来再新建文件。

适用场景：

- 只在当前 Widget 内使用
- 想提升 `build` 可读性
- 没必要抽成独立跨文件组件

## 强制规则

### 1. `view.dart` 只做组合和事件入口

主页面应该像这样：

```dart
class FeaturePage extends StatelessWidget {
  const FeaturePage({super.key});

  @override
  Widget build(BuildContext context) {
    return buildPageBg(children: [
      buildTopArea(children: [
        FeatureNavigation(
          data: state.navigation,
          onTap: (item) => logic.onNavigationTap(item),
        ),
        buildScrollableContent(children: [
          FeatureHeader(
            data: state.header,
            onSearchChanged: logic.onSearchChanged,
            onRefresh: logic.onRefresh,
          ),
          FeatureBanner(
            data: state.bannerList,
            onTap: logic.onBannerTap,
          ),
          FeatureGuess(
            data: state.guessList,
            onChange: logic.onGuessChange,
            onItemTap: logic.onGuessTap,
          ),
        ]),
      ]),
      FeatureBottomBar(
        data: state.bottomBar,
        onPlay: logic.onPlay,
      ),
    ]);
  }
}
```

这个层面允许有嵌套，但只能是**业务组合层级**，不能退化成“把所有细节直接写在这里”。

### 2. 非通用业务 Widget 尽量只收一个主数据源

业务 Widget 优先：

- `data + callbacks`

不要默认拆成十几个基础字段。

```dart
class FeatureGuess extends StatelessWidget {
  const FeatureGuess({
    super.key,
    required this.data,
    required this.onChange,
    required this.onItemTap,
  });

  final List<FeatureItem> data;
  final VoidCallback onChange;
  final ValueChanged<FeatureItem> onItemTap;
}
```

例外：

- 通用组件
- 设计系统组件
- 需要跨多模块复用的低耦合组件

### 3. 所有交互事件必须上提暴露

用户交互不能悄悄消化在 UI 内部。

必须暴露的典型事件：

- `onTap`
- `onChanged`
- `onRefresh`
- `onLoadMore`
- `onRetry`
- `onSortTitle`

目标是让你只看 `view.dart`，就能看到页面主要交互入口。

### 4. 业务 Widget 的 `build` 只保留结构

```dart
@override
Widget build(BuildContext context) {
  return _buildBg(children: [
    _buildHeader(),
    _buildItemBg(itemBuilder: (item) {
      return [
        _buildPicCard(item),
        _buildTitle(item),
        _buildSubTitle(item),
      ];
    }),
  ]);
}
```

要求：

- `children` 里的每个块都应该有明确名字
- 复杂区块建议在 `children` 中写注释
- `_buildBg` 负责封装 margin、padding、对齐等无关主结构的细节

### 5. 单层列表必须用 builder 反传数据

```dart
Widget _buildItemBg({
  required List<Widget> Function(FeatureItem item) itemBuilder,
}) {
  return Row(
    children: List.generate(data.length, (index) {
      return Column(children: itemBuilder(data[index]));
    }),
  );
}
```

规则：

- 列表容器负责循环
- 具体 item 结构通过 `itemBuilder` 回传
- 不要把完整 `List.generate(...)` 直接糊在主 `build` 的 `children` 中

### 6. 双层列表必须拆成 `itemBuilder + subBuilder`

```dart
Widget _buildItemListBg({
  required List<Widget> Function(FeatureGroup item) itemBuilder,
}) {
  return Column(
    children: List.generate(data.length, (index) {
      return Column(children: itemBuilder(data[index]));
    }),
  );
}

Widget _buildSubItemListBg(
  FeatureGroup item, {
  required List<Widget> Function(FeatureItem subItem) subBuilder,
}) {
  return Column(
    children: List.generate(item.items.length, (index) {
      return InkWell(
        onTap: () => onTap(item.items[index]),
        child: Row(children: subBuilder(item.items[index])),
      );
    }),
  );
}
```

双层列表不这样拆，代码很快就会重新长回去。

### 7. 状态管理实现不改变这套 view 规则

无论 `logic.dart` 内部是：

- 轻逻辑层
- Cubit
- Bloc

都应该保持：

- view 只看业务结构
- 业务事件统一向上暴露
- 布局骨架单独封装

## 推荐工作流

1. 先读当前页面，标出页面级业务区块
2. 找出所有用户交互点，确认哪些事件需要上提
3. 先抽 `view.dart` 的稳定骨架到 `widget/[module]_function.dart`
4. 再按业务含义拆 `widget/*.dart`，不要按视觉碎片乱拆
5. 进入每个业务 Widget，把 `children` 重写成 `_buildXxx()` 结构
6. 遇到单层列表，用 `itemBuilder`
7. 遇到双层列表，用 `itemBuilder + subBuilder`
8. 回头检查 `view.dart` 是否只剩“业务组合 + 事件入口”

## 禁忌项

- 只是把一大段代码提成 `_buildFoo()`，但 `view.dart` 里仍然是海量细节
- 每个小图标、小文字都新建单独文件，拆得只剩碎片
- 业务 Widget 内部直接调用 `logic`
- 一个业务 Widget 传十几个字段，丢掉业务语义
- 把 `List.generate / map / Wrap / Row / Column / GestureDetector` 全堆在主页面 `children`
- 把 `_buildBg`、滚动容器、`Expanded`、`Scrollbar` 这些脚手架细节留在主页面里

## 验收清单

- [ ] `view.dart` 能在一屏内看懂大致结构
- [ ] `view.dart` 中能直接看到主要事件入口
- [ ] 稳定骨架已抽到 `widget/[module]_function.dart`
- [ ] 业务区块已拆成有业务语义的 Widget
- [ ] 业务 Widget 内部 `children` 基本都是 `_buildXxx()`
- [ ] 单层列表已使用 `itemBuilder`
- [ ] 双层列表已使用 `itemBuilder + subBuilder`
- [ ] 修改某个区块样式时，可以在 1 次跳转内定位到对应 Widget

## 一句话原则

**统一命名为 `logic.dart`，主页面看组合，function 看骨架，widget 看区块，builder 吃列表。**
