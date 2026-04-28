---
name: flutter-no-nesting
description: 用于编写、重构或评审 Flutter 页面结构，尤其当页面出现“嵌套过深”“套娃”“widget tree 过长”“页面难维护”时使用。适用于把复杂页面重构为“页面组合 + 布局骨架函数 + 业务 Widget + 列表 builder”结构。
version: 2.0.0
---

# Flutter 页面去嵌套

基于《Flutter 改善套娃地狱问题（仿喜马拉雅PC页面举例）》的方法论，这个 skill 的目标不是“把代码拆得更碎”，而是把页面改造成**可读、可改、可定位事件入口**的结构。

核心思想：**按业务分块组合 Widget，用外观模式管理页面，而不是把整页 UI 直接写成一棵深层 Widget 树。**

## 什么时候用

出现下列任一情况时使用本 skill：

- 页面 `build` 方法超过一屏，阅读时需要来回找括号。
- 页面同时混着布局细节、业务区块、列表遍历和点击事件。
- 想改某个局部样式或交互，但很难快速定位入口。
- 页面已经按状态管理分层，但 UI 结构依然是“大段套娃”。
- 需要把已有 Flutter 页面重构成更稳定的多人协作结构。

## 目标结果

重构后的页面应满足：

- 主页面只保留“业务区块组合”和“事件入口转发”。
- 布局骨架细节从主页面移走，收敛到 `xxx_function.dart` 或局部 `_buildBg`。
- 每个业务区块有明确输入数据和明确回调。
- 列表 UI 不在 `children` 里直接硬展开，而是通过 `itemBuilder` / `subBuilder` 组织。
- 看到主页面或业务 Widget 的 `build`，就能快速看懂页面结构。

## 拆分决策

先判断你要抽出来的东西属于哪一层：

### 1. 页面层

适合放：

- 业务区块组合顺序
- 页面级状态读取
- 所有用户事件的统一出口

不适合放：

- 大段 `Container / Padding / Row / Column / Expanded`
- 列表遍历细节
- 某个局部区块的样式实现

### 2. 布局骨架函数

适合抽成函数，通常放在 `xxx_function.dart`：

- `Scaffold`
- 页面主 `Row / Column`
- 滚动区外壳
- 反复出现但业务含义弱的布局容器

这类函数的特点是：**结构稳定、业务含义弱、写完后很少改。**

示例：

```dart
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

### 3. 业务 Widget

适合抽成独立 Widget：

- 顶部搜索区
- 轮播区
- 猜你喜欢
- 榜单区
- 底部操作栏

这类 Widget 必须体现业务含义，而不是只按“一个 `Container`”来拆。

### 4. Widget 内部私有方法

业务 Widget 内部的 `children` 项，优先提成 `_buildXxx()` 方法，而不是继续向外拆文件。

适合提成私有方法的场景：

- 只在当前 Widget 内使用
- 业务意义明确，但没有必要单独成为公共组件
- 目的是让 `build` 结构变清晰，而不是追求组件数量

## 强制规则

### 1. 主页面只做组合和转发

主页面的 `build` 应只保留业务区块排列，以及把事件转发给 `logic / bloc / controller / cubit`。

```dart
class MyPage extends StatelessWidget {
  const MyPage({super.key});

  @override
  Widget build(BuildContext context) {
    return buildPageBg(children: [
      MyHeader(
        data: state.header,
        onSearch: logic.onSearch,
        onRefresh: logic.onRefresh,
      ),
      MyContentList(
        data: state.items,
        onItemTap: logic.onItemTap,
      ),
      MyBottomBar(
        data: state.bottomBar,
        onActionTap: logic.onActionTap,
      ),
    ]);
  }
}
```

判断标准：如果主页面开始出现大量 `padding`、`margin`、`alignment`、列表遍历或长链式嵌套，就说明还没拆干净。

### 2. 业务 Widget 尽量只收一个数据源

对于非通用业务 Widget，优先传一个业务数据对象，而不是十几个零散字段。

- 业务 Widget：优先 `data + callbacks`
- 通用组件：才考虑细粒度字段输入

```dart
class MySection extends StatelessWidget {
  const MySection({
    super.key,
    required this.data,
    required this.onItemTap,
    required this.onChange,
  });

  final MySectionData data;
  final ValueChanged<ItemInfo> onItemTap;
  final VoidCallback onChange;
}
```

### 3. 所有交互必须显式暴露

不要把点击、切换、滚动触发的业务行为悄悄消化在业务 Widget 内部。

必须暴露：

- `onTap`
- `onChanged`
- `onRefresh`
- `onLoadMore`
- 其他会触发业务状态变化的事件

目标是让主页面一眼看到完整的事件入口。

### 4. 业务 Widget 的 `build` 只保留结构

一个业务 Widget 的 `build` 里，`children` 应尽量全是 `_buildXxx()`。

```dart
class MySection extends StatelessWidget {
  const MySection({
    super.key,
    required this.data,
    required this.onItemTap,
  });

  final MySectionData data;
  final ValueChanged<ItemInfo> onItemTap;

  @override
  Widget build(BuildContext context) {
    return _buildBg(children: [
      // 标题栏
      _buildHeader(),
      // 内容列表
      _buildItemList(),
      // 底部按钮
      _buildFooter(),
    ]);
  }

  Widget _buildBg({required List<Widget> children}) {
    return Container(
      margin: const EdgeInsets.all(16),
      child: Column(children: children),
    );
  }
}
```

要求：

- `children` 里的每个块有清晰名字。
- 复杂业务 Widget 建议给每个块加一行注释。
- `_buildBg` 负责吃掉与主结构无关的容器细节。

### 5. 单层列表用 `itemBuilder` 回传数据

列表型区块不要把遍历逻辑直接糊在 `build` 里。把列表容器和 item 展开分开写。

```dart
Widget build(BuildContext context) {
  return _buildBg(children: [
    _buildHeader(),
    _buildItemBg(itemBuilder: (item) {
      return [
        _buildImage(item),
        _buildTitle(item),
        _buildSubtitle(item),
      ];
    }),
  ]);
}

Widget _buildItemBg({
  required List<Widget> Function(ItemInfo item) itemBuilder,
}) {
  return Row(
    children: List.generate(data.items.length, (index) {
      return Column(children: itemBuilder(data.items[index]));
    }),
  );
}
```

重点不是“必须叫 `itemBuilder`”，而是**列表容器负责遍历，具体 item 内容通过回调回传**。

### 6. 双层列表用 `itemBuilder + subBuilder`

如果列表的每个 item 里还有子列表，外层和内层都要分开。

```dart
Widget build(BuildContext context) {
  return _buildBg(children: [
    _buildOuterList(itemBuilder: (group) {
      return [
        _buildGroupTitle(group.title),
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
  required List<Widget> Function(GroupInfo group) itemBuilder,
}) {
  return Column(
    children: List.generate(data.groups.length, (index) {
      return Column(children: itemBuilder(data.groups[index]));
    }),
  );
}

Widget _buildInnerList(
  GroupInfo group, {
  required List<Widget> Function(ItemInfo item) subBuilder,
}) {
  return Column(
    children: List.generate(group.items.length, (index) {
      return Row(children: subBuilder(group.items[index]));
    }),
  );
}
```

## 推荐工作流

当用户要求“去嵌套”“重构页面结构”时，按这个顺序执行：

1. 先读页面，找出页面级业务区块。
2. 标出所有用户交互入口，决定哪些事件需要上提。
3. 把 `Scaffold`、主 `Row / Column`、滚动骨架抽到函数层。
4. 按业务含义拆出业务 Widget，不按纯视觉碎片乱拆。
5. 把业务 Widget 内部 `children` 提成 `_buildXxx()`。
6. 把单层或双层列表改成 builder 模式。
7. 回头压缩主页面，直到主页面只剩“组合 + 事件转发”。

## 禁忌项

不要做这些事：

- 只是把一大段 Widget 提成 `_buildFoo()`，但页面仍然保留所有业务细节。
- 每个小图标、小文字都拆成单独文件，导致结构更碎。
- 业务 Widget 内部直接调用外部逻辑层而不暴露回调。
- 一个业务 Widget 传十几个基础类型参数，失去业务语义。
- 把列表遍历、点击事件、布局细节全部堆在同一个 `children` 里。
- 为了“减少嵌套”而牺牲语义，写出一堆难懂的抽象函数名。

## 输出要求

使用本 skill 时，产出的 Flutter 代码应尽量满足以下目录结构：

```text
my_page/
├── my_page.dart
├── my_page_function.dart
├── my_page_logic.dart
├── my_page_state.dart
└── widgets/
    ├── my_header.dart
    ├── my_section.dart
    └── my_bottom_bar.dart
```

说明：

- `my_page.dart`：页面组合、状态读取、事件转发
- `my_page_function.dart`：稳定布局骨架
- `widgets/`：业务 Widget
- `logic/state`：状态和交互处理

如果项目已有既定架构，例如 BLoC、Riverpod、MVVM、GetX，只迁移 UI 组织方式，不强推状态管理方案。

## 评审清单

完成后按下面自查：

- [ ] 主页面 `build` 是否能在一屏内看懂？
- [ ] 主页面是否只保留业务区块组合和事件入口？
- [ ] 布局骨架是否已经从主页面移走？
- [ ] 每个业务 Widget 是否只有明确的数据输入和回调输入？
- [ ] 业务 Widget 的 `children` 是否基本都是 `_buildXxx()`？
- [ ] 列表区块是否用了 builder 思路，而不是在页面里直接套多层循环？
- [ ] 修改某个区块样式时，是否能在 1 次跳转内定位到对应实现？

## 一句话原则

**页面看业务结构，Widget 看区块细节，函数吃布局骨架，事件统一上提。**
