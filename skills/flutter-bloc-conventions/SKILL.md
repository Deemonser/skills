---
name: flutter-bloc-conventions
description: 用于编写、重构或评审基于 flutter_bloc 的 Flutter 页面代码。仅在用户明确要求实现、重构、修复、评审 Flutter 页面状态管理代码，并且需要实际修改 `logic / state / event / data` 结构时使用。约束内容包括：`logic.dart + state.dart + view.dart + widget/` 的轻量目录、Bloc/Cubit 选择、事件与状态设计、provider 生命周期、数据流边界、副作用与重建分离、以及 bloc_test 测试规范。view 层结构细则依赖 flutter-view-conventions。不用于闲聊、概念讨论、框架比较或未进入实现阶段的方案交流。
version: 5.0.0
---

# Flutter BLoC Conventions

这个 skill 约束 **BLoC/Cubit 分层、数据流、provider 生命周期、副作用处理、重建控制、测试方式**，并要求 view 层遵循 `flutter-view-conventions`。

目标：

- 状态管理职责明确
- 数据流可追踪
- UI 不夹带业务逻辑
- view 层结构清晰
- 命名和目录稳定，不在 `logic / cubit / bloc` 之间来回切换

## 什么时候用

- 用户明确要求修改基于 `flutter_bloc` 的 Flutter 页面代码
- 当前任务需要实际调整 `logic / state / event / data` 结构
- 需要设计或重构状态流、事件流、provider 生命周期、bloc 测试

不要用于：

- 闲聊
- 纯概念讨论
- 框架比较
- 尚未进入实现阶段的方案交流

## 命名约定

统一使用这套文件名：

```text
feature/
├── logic.dart
├── state.dart
├── view.dart
└── widget/
    ├── feature_function.dart
    ├── feature_section_a.dart
    └── ...
```

当页面进入明确的事件流模式时，再增加：

```text
feature/
├── event.dart
```

含义：

- `logic.dart`：统一的逻辑层坑位
- `state.dart`：页面状态
- `view.dart`：页面主入口
- `event.dart`：仅在 Bloc 式事件流下存在

也就是说：

- 简单状态时，`logic.dart` 里通常定义 `Cubit`
- 复杂事件流时，`logic.dart` 里通常定义 `Bloc`
- 只有事件流模式才额外增加 `event.dart`

## 先做判断

### 直接用 `logic.dart` + `Cubit`

适合：

- tab / 开关 / 局部表单
- 单页加载 / 刷新 / 重试
- 没有复杂事件语义，但不想把逻辑塞回 widget

### `logic.dart` + `event.dart` + `Bloc`

适合：

- 初始化加载
- 刷新 / 分页 / 重试
- 提交 / 删除 / 撤销
- 搜索、防抖、取消旧请求
- 多来源事件驱动同一页面

没有复杂事件语义时，优先 Cubit。

## 目录结构

### 核心结构

默认保持轻量目录：

```text
feature/
├── logic.dart
├── state.dart
├── view.dart
└── widget/
    ├── feature_function.dart
    ├── feature_section_a.dart
    └── ...
```

### 按需扩展

1. 复杂事件流时，加 `event.dart`
2. 涉及网络请求、多数据源、缓存、统一错误语义时，再扩展：

```text
feature/
├── data/
│   ├── repositories/
│   ├── datasources/
│   └── models/
```

规则：

- 目录可以轻，但职责不能轻
- 本地状态或单一 service 调用时，可以不建 `data/`
- 一旦引入 `Repository / Datasource`，就必须遵守边界

## 分层职责

### `view.dart`

负责：提供 provider、消费状态、派发事件/方法、组织页面结构、承接导航和提示类副作用。  
不负责：直接发请求、编排业务流程、做数据映射、写大段嵌套 UI。

### `widget/`

负责具体业务区块。

- `feature_function.dart`：稳定布局骨架
- `feature_section_x.dart`：业务区块

业务 Widget 只接收展示数据和回调，不直接依赖 repository 或 datasource。

### `logic.dart`

负责：接收页面动作、驱动状态变化、编排流程、调用 repository/service、输出可消费状态。  
不负责：直接调用 SDK / client，或写 Widget。

实现方式：

- 简单状态：`class FeatureLogic extends Cubit<FeatureState>`
- 复杂事件流：`class FeatureLogic extends Bloc<FeatureEvent, FeatureState>`

### `state.dart`

负责页面可渲染状态。应包含：

- `loading / success / failure`
- 页面展示数据
- 错误信息、空态、局部选中态、分页状态

不要包含：

- `BuildContext`
- `Widget`
- `TextEditingController`
- `FocusNode`
- 原始后端 DTO 直接污染 UI 状态

### `event.dart`

只在 Bloc 模式存在。Event 表达页面动作，不是函数名。

推荐：

- `FeatureStarted`
- `FeatureRefreshed`
- `FeatureLoadMoreRequested`
- `SearchTextChanged`
- `FormSubmitted`

不推荐：

- `GetData`
- `DoSomething`
- `UpdateState`

### `Repository`

负责：编排多个数据源、做 DTO 映射、统一错误语义。  
不负责：持有 UI 状态、写 Widget 逻辑。

### `Datasource`

负责底层调用，例如 REST / GraphQL / SQLite / Isar / Hive / Supabase / Firebase / 本地缓存访问。  
不负责业务编排和 UI 状态组织。

## 数据流

Cubit 模式：

```text
UI action → logic.dart(Cubit) → state.dart → View
```

Bloc 模式：

```text
UI action → event.dart → logic.dart(Bloc) → state.dart → View
```

如果有数据层：

```text
UI action
→ Logic
→ Repository
→ Datasource
→ Repository 映射结果
→ Logic emit 新状态
→ View 渲染
```

禁止：

- `View` 直接调 `Datasource`
- `Repository` 持有 `BuildContext`
- `Logic` 直接依赖另一个 `Logic`

## Provider 生命周期

页面自己拥有 logic 时，用 `BlocProvider(create:)`。它会负责关闭实例。

```dart
BlocProvider(
  create: (context) => FeatureLogic(
    repository: context.read<FeatureRepository>(),
  )..refresh(),
  child: const _FeatureBody(),
);
```

如果 `FeatureLogic` 是 `Bloc`，就把 `..refresh()` 换成 `..add(const FeatureStarted())`。

把已有实例传给新 route、dialog、bottom sheet 时，用 `BlocProvider.value`，它不会自动关闭实例。

```dart
BlocProvider.value(
  value: context.read<FeatureLogic>(),
  child: const FeatureDetailPage(),
);
```

多个 provider/listener 并列时用 `MultiBlocProvider`、`MultiBlocListener`、`MultiRepositoryProvider`，不要写 provider 套娃。

## View 规则

view / widget 结构细则遵循 `flutter-view-conventions`，这里不重复展开，只强调：

- 页面骨架先建立，再挂状态消费工具
- 复杂区块拆进 `widget/`
- `BlocBuilder / BlocListener / BlocConsumer / BlocSelector` 不应主导整页骨架

`view.dart` 可以保持单文件，不强制拆 `page.dart + view.dart`；但至少要做到 provider 注入和页面 body 分层、页面骨架先建立、状态消费工具下沉到区块。

```dart
class FeaturePage extends StatelessWidget {
  const FeaturePage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => FeatureLogic(
        repository: context.read<FeatureRepository>(),
      )..refresh(),
      child: const _FeatureBody(),
    );
  }
}

class _FeatureBody extends StatelessWidget {
  const _FeatureBody();

  @override
  Widget build(BuildContext context) {
    return buildFeaturePage(children: [
      _buildHeaderSection(),
      _buildBodySection(),
    ]);
  }

  Widget _buildHeaderSection() {
    return BlocSelector<FeatureLogic, FeatureState, HeaderData>(
      selector: (state) => state.header,
      builder: (context, header) {
        return FeatureHeader(
          data: header,
          onRefresh: () => context.read<FeatureLogic>().refresh(),
        );
      },
    );
  }

  Widget _buildBodySection() {
    return BlocConsumer<FeatureLogic, FeatureState>(
      listenWhen: (previous, current) =>
          previous.errorMessage != current.errorMessage,
      listener: (context, state) {
        if (state.errorMessage != null) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.errorMessage!)),
          );
        }
      },
      buildWhen: (previous, current) => previous.sections != current.sections,
      builder: (context, state) {
        return FeatureBody(
          data: state.sections,
          isLoading: state.status == FeatureStatus.loading,
          onRetry: () => context.read<FeatureLogic>().refresh(),
          onItemTap: (item) => context.read<FeatureLogic>().openItem(item),
        );
      },
    );
  }
}
```

副作用和重建分开：

- 仅重建 UI：`BlocBuilder`
- 仅副作用：`BlocListener`
- 两者都有：`BlocConsumer`
- 只关心局部字段：`BlocSelector`

事件派发用 `context.read`，不要在回调里用 `watch`。

## 状态与实现规则

状态常用两种：

- 单状态类 + `status enum`
- 多子类状态

大部分字段共享时，优先单状态类：

```dart
enum FeatureStatus { initial, loading, success, failure }

class FeatureState extends Equatable {
  const FeatureState({
    this.status = FeatureStatus.initial,
    this.items = const [],
    this.errorMessage,
  });

  final FeatureStatus status;
  final List<Item> items;
  final String? errorMessage;

  FeatureState copyWith({
    FeatureStatus? status,
    List<Item>? items,
    String? errorMessage,
  }) {
    return FeatureState(
      status: status ?? this.status,
      items: items ?? this.items,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }

  @override
  List<Object?> get props => [status, items, errorMessage];
}
```

如果不同状态的数据结构差异很大，再用多子类状态。

状态和事件必须具备稳定值语义。通常使用 `Equatable` 或项目已有的等价不可变方案，不要原地修改可变对象。

异步流程必须显式表达 `initial / loading / success / failure`。错误状态至少应提供用户可展示的信息和 UI 可判定的失败状态。

Logic 不直接做底层调用：

```dart
final data = await repository.fetchItems();
```

不要在 logic/state/event 中出现：

- `TextEditingController`
- `BuildContext`
- `Color`
- `Widget`

## 测试规范

优先使用 `package:bloc_test` 和 `package:mocktail`。

无论 `logic.dart` 内部是 Cubit 还是 Bloc，都优先用 `blocTest`。

至少覆盖：

- 初始状态
- 成功路径
- 失败路径
- 重试或刷新路径
- 关键状态序列

```dart
blocTest<FeatureLogic, FeatureState>(
  'emit [loading, success] when request succeeds',
  build: () => FeatureLogic(repository: repository),
  act: (logic) => logic.refresh(),
  expect: () => [
    isA<FeatureState>().having(
      (state) => state.status,
      'status',
      FeatureStatus.loading,
    ),
    isA<FeatureState>().having(
      (state) => state.status,
      'status',
      FeatureStatus.success,
    ),
  ],
);
```

如果 `FeatureLogic` 是 Bloc，则把 `act` 换成 `logic.add(const FeatureStarted())`。

## 推荐工作流

1. 先判断 `logic.dart` 内部该用 `Cubit` 还是 `Bloc`
2. 先设计 `state.dart`，再写 UI
3. 如果是事件流模式，再补 `event.dart`
4. 明确是否需要 `data/repositories` 和 `data/datasources`
5. 写 `view.dart` 提供 logic
6. 按 `flutter-view-conventions` 拆出 `widget/` 下的业务区块
7. 把状态消费工具嵌进具体区块
8. 为 logic 写测试

## 禁忌项

- 在 `View` 里直接请求接口
- 在 `view.dart` 里写整页复杂 UI 细节
- 在 `logic.dart` 里直接调 SDK
- 一个 `build` 里堆满 `BlocConsumer + Column + Expanded + Padding + List.generate + InkWell`
- 事件名、状态名没有业务语义
- 失败状态没有落到 UI 可消费结构
- 为了用 BLoC 而用 BLoC，简单局部状态也强行上事件流

## 提交前检查

- [ ] 已判断 `logic.dart` 内部该用 `Cubit` 还是 `Bloc`
- [ ] 目录结构采用核心结构，必要时才扩展 `event.dart` 和 `data/`
- [ ] `view.dart` 负责提供 logic 并组织页面，内部职责分离清楚
- [ ] view 层结构遵循 `flutter-view-conventions`
- [ ] `logic.dart` 不直接调用 SDK
- [ ] 引入 `Repository / Datasource` 时边界清楚
- [ ] 事件和状态命名有明确业务语义
- [ ] 异步流程能区分 loading / success / failure
- [ ] 错误状态能被 UI 正常消费
- [ ] Provider 生命周期处理正确
- [ ] 重建范围和副作用边界清楚
- [ ] 测试覆盖关键状态流

## 一句话原则

**统一命名为 `logic.dart`，简单状态用 Cubit，复杂事件流再加 `event.dart`。**
