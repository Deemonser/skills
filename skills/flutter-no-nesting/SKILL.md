---
name: flutter-no-nesting
description: This skill should be used when writing or reviewing Flutter UI code, especially when the user mentions "嵌套", "套娃", "nesting hell", "widget tree", or asks to refactor/structure a Flutter page. Applies when building complex Flutter pages with multiple sections, lists, or interactive elements.
version: 1.0.0
---

# Flutter 页面去嵌套方法论

解决 Flutter "套娃地狱"的核心思想：**外观模式（Facade Pattern）** — 把页面拆成业务 Widget 组合，而不是一棵无限深的 Widget 树。

## 核心原则

### 1. 主页面只做两件事
- 组合业务 Widget
- 集中所有交互事件入口（全部转发给 logic 层）

```dart
class MyPage extends StatelessWidget {
  final logic = Get.put(MyLogic());
  final state = Get.find<MyLogic>().state;

  @override
  Widget build(BuildContext context) {
    return _buildBg(children: [
      // 顶部区域
      MyHeader(
        data: state.headerData,
        onSearch: (msg) => logic.onSearch(msg),   // 事件集中暴露
        onRefresh: () => logic.onRefresh(),
      ),

      // 内容列表
      MyContentList(
        data: state.contentList,
        onItemTap: (item) => logic.onItemTap(item),
        onLoadMore: () => logic.onLoadMore(),
      ),

      // 底部操作栏
      MyBottomBar(
        data: state.bottomInfo,
        onAction: () => logic.onAction(),
      ),
    ]);
  }
}
```

### 2. 布局骨架单独封装（`xxx_function.dart`）

把 Scaffold / Expanded / Row / Column 这些"脚手架"提取成函数，只暴露 `children`：

```dart
// my_page_function.dart
Widget buildPageBg({required List<Widget> children}) {
  return Scaffold(
    backgroundColor: Colors.white,
    body: Column(children: children),
  );
}

Widget buildScrollSection({required List<Widget> children}) {
  return Expanded(
    child: SingleChildScrollView(
      child: Column(children: children),
    ),
  );
}
```

这些写完后基本不再改动，放着"吃灰"即可。

### 3. 业务 Widget 封装规则

**数据源**：业务 Widget 尽量只接受一个数据对象（非通用组件）。通用组件才细分字段。

**交互事件**：所有 onXxx 回调必须暴露出来，不能内部消化。

**内部结构**：children 里每个子 Widget 提成独立的 `_buildXxx()` 方法，并加注释。

```dart
class MySection extends StatelessWidget {
  MySection({
    required this.data,
    required this.onItemTap,   // 事件必须暴露
    required this.onChange,
  });

  final MySectionData data;
  final void Function(ItemInfo) onItemTap;
  final VoidCallback onChange;

  @override
  Widget build(BuildContext context) {
    return _buildBg(children: [
      // 标题栏
      _buildHeader(),

      // 内容卡片列表
      _buildCardList(),

      // 底部按钮
      _buildFooterBtn(),
    ]);
  }

  // 布局容器细节封装在此，不污染 build 方法
  Widget _buildBg({required List<Widget> children}) {
    return Container(
      margin: EdgeInsets.all(16),
      child: Column(children: children),
    );
  }

  Widget _buildHeader() { ... }
  Widget _buildFooterBtn() { ... }

  // 列表类：用 itemBuilder 回调反传遍历数据
  Widget _buildCardList() {
    return Row(
      children: List.generate(data.items.length, (index) {
        return Column(
          children: _buildCardItem(data.items[index]),
        );
      }),
    );
  }

  List<Widget> _buildCardItem(ItemInfo item) {
    return [
      // 图片
      _buildImage(item),
      // 标题
      Text(item.title),
      // 副标题
      _buildSubTitle(item),
    ];
  }
}
```

## 双层列表封装（嵌套列表）

当列表的每个 item 内部还有一个列表时，用 `itemBuilder` + `subBuilder` 两层回调：

```dart
Widget build(BuildContext context) {
  return _buildBg(children: [
    _buildOuterList(itemBuilder: (group) {
      return [
        // 分组标题
        _buildGroupTitle(group.title),

        // 分组内的子列表
        _buildInnerList(group, subBuilder: (item) {
          return [
            _buildIcon(item),
            _buildLabel(item),
          ];
        }),
      ];
    }),
  ]);
}

Widget _buildOuterList({
  required List<Widget> Function(GroupInfo) itemBuilder,
}) {
  return Expanded(
    child: Scrollbar(
      child: SingleChildScrollView(
        child: Column(
          children: List.generate(data.groups.length, (i) {
            return Column(children: itemBuilder(data.groups[i]));
          }),
        ),
      ),
    ),
  );
}

Widget _buildInnerList(
  GroupInfo group, {
  required List<Widget> Function(ItemInfo) subBuilder,
}) {
  return Column(
    children: List.generate(group.items.length, (i) {
      return InkWell(
        onTap: () => onItemTap(group.items[i]),
        child: Row(children: subBuilder(group.items[i])),
      );
    }),
  );
}
```

## 文件结构

```
my_page/
├── my_page.dart           # 主页面：只做组合 + 事件转发
├── my_page_function.dart  # 布局骨架函数（Scaffold/Row/Column 封装）
├── my_page_logic.dart     # 业务逻辑
├── my_page_state.dart     # 状态数据
└── widgets/
    ├── my_header.dart     # 业务 Widget
    ├── my_section.dart
    └── my_bottom_bar.dart
```

## 检查清单

写完一个页面后自查：

- [ ] 主页面的 `build` 方法能一屏看完吗？
- [ ] 所有 onXxx 事件都在主页面集中可见吗？
- [ ] 每个业务 Widget 内部的 `build` 里，children 都是 `_buildXxx()` 方法调用吗？
- [ ] 布局骨架细节（padding/margin/颜色等）都封装进了 `_buildBg` 类方法吗？
- [ ] 列表遍历都用了 `itemBuilder` 回调模式吗？

## 快速提取技巧（IDE）

在 Android Studio / VS Code 中：
1. 选中要提取的 Widget 代码块
2. 打开 Flutter Outline 面板
3. 点击 **Extract Method**（右箭头图标）
4. 填入方法名，自动生成带参数的 `_buildXxx()` 方法
