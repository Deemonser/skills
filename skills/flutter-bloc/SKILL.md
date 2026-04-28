---
name: flutter-bloc-development
description: 用于编写、重构或评审基于 Flutter BLoC/Cubit 的功能代码。适用于新功能开发、页面接入状态管理、重构 UI 与逻辑分层，或审查事件/状态/数据流是否清晰。view 层必须同时遵循 flutter-no-nesting 的页面组织方式。
version: 2.0.0
---

# Flutter BLoC 开发规范

这个 skill 用来约束 **BLoC/Cubit 分层、数据流、测试方式，以及 view 层和 `flutter-no-nesting` 的配合方式**。

它不是一篇 BLoC 教程。目标是让产出的代码满足：

- 状态管理职责明确
- 数据流可追踪
- UI 不夹带业务逻辑
- view 层结构清晰，不写成大段套娃

## 什么时候用

出现以下任一情况时使用：

- 新建一个使用 `flutter_bloc` 的功能或页面
- 给已有页面接入 `Bloc` 或 `Cubit`
- 重构 `Page / View / Widgets / Bloc / Repository / Datasource`
- 评审 Flutter 代码是否把业务逻辑错误地写进了 UI
- 修复事件命名混乱、状态不可追踪、测试缺失的问题

## 配合规则

### view 层必须遵循 `flutter-no-nesting`

只要本 skill 涉及 Flutter 页面或组件实现，就必须同时遵守 `flutter-no-nesting` 的规则：

- `Page` 和 `View` 只保留业务结构、状态消费和事件派发
- 复杂布局必须拆成业务 Widget 组合
- 列表区块使用 builder 思路组织
- 不能把长链式 `Row / Column / Padding / Expanded / ScrollView` 全堆在一个 `build`

一句话：

**BLoC skill 负责状态流，no-nesting skill 负责 view 结构。**

## 先做判断

开始写之前先判断这次任务属于哪种：

### 1. 简单局部状态

如果只是：

- tab 切换
- 开关状态
- 计数器
- 表单局部可见性
- 没有复杂异步事件链

优先用 `Cubit`。

### 2. 复杂事件流或异步流程

如果涉及：

- 初始化加载
- 刷新 / 分页 / 重试
- 表单提交
- 多状态切换
- 明确的事件语义和调试追踪

使用 `Bloc`。

## 推荐目录

默认采用功能优先结构：

```text
lib/
└── feature/
    ├── bloc/
    │   ├── feature_bloc.dart
    │   ├── feature_event.dart
    │   └── feature_state.dart
    ├── data/
    │   ├── datasources/
    │   ├── repositories/
    │   └── models/
    ├── view/
    │   ├── feature_page.dart
    │   ├── feature_view.dart
    │   └── widgets/
    └── feature.dart
```

如果项目已有既定目录规范，优先跟随项目，不强推这个结构。但职责边界不能丢。

## 分层职责

### 1. Page

`Page` 只负责：

- 创建 `BlocProvider` / `MultiBlocProvider`
- 组装依赖
- 挂载 `View`

`Page` 不负责：

- 写业务 UI 细节
- 直接渲染复杂页面结构
- 写事件处理逻辑

```dart
class FeaturePage extends StatelessWidget {
  const FeaturePage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => FeatureBloc(
        repository: context.read<FeatureRepository>(),
      )..add(const FeatureStarted()),
      child: const FeatureView(),
    );
  }
}
```

### 2. View

`View` 只负责：

- 消费 BLoC 状态
- 派发用户事件
- 组织页面结构
- 承担必要副作用入口，例如 `SnackBar`、导航、弹窗

`View` 不负责：

- 直接发请求
- 编排业务流程
- 做数据映射
- 写大段嵌套 UI

### 3. Feature Widgets

业务 Widget 只负责表现层细节：

- 接收展示数据
- 接收回调
- 内部结构清晰

不要让业务 Widget 直接依赖 repository 或 datasource。

### 4. Bloc / Cubit

负责：

- 接收事件或方法调用
- 驱动状态变化
- 编排 use case
- 调用 repository
- 输出可消费状态

不负责：

- 直接调用 SDK / HTTP client / Supabase client
- 写 Widget

### 5. Repository

负责：

- 编排多个数据源
- DTO 到领域对象的映射
- 统一错误转换

不负责：

- 持有 UI 状态
- 写 Widget 相关逻辑

### 6. Datasource

负责：

- 直接调用 SDK / API / 数据库存取

不负责：

- 业务编排
- UI 可读状态的组织

## 数据流

标准数据流：

```text
UI event
→ Bloc/Cubit
→ Repository
→ Datasource
→ Repository 映射结果
→ Bloc/Cubit emit 新状态
→ View 渲染
```

禁止以下反向污染：

- `View` 直接调 `Datasource`
- `Repository` 持有 `BuildContext`
- `Bloc` 直接依赖另一个 `Bloc`

如果多个 BLoC 需要共享信息，优先通过以下方式解决：

- 共享 repository
- UI 层协调派发事件
- 更上层的组合 bloc/cubit

## View 层实现规则

### 1. Page / View 强制分离

- `feature_page.dart`：创建并提供 bloc
- `feature_view.dart`：消费状态并组织页面

### 2. View 必须按 no-nesting 组织

`feature_view.dart` 里：

- 主 `build` 只保留业务区块结构
- 大块布局骨架抽成函数或业务 Widget
- 事件通过 `context.read<FeatureBloc>().add(...)` 派发
- 页面里的业务区块拆进 `view/widgets/`
- `BlocBuilder / BlocListener / BlocConsumer / BlocSelector` 属于状态消费工具，不应主导页面骨架

示例：

```dart
class FeatureView extends StatelessWidget {
  const FeatureView({super.key});

  @override
  Widget build(BuildContext context) {
    return _buildPage(children: [
      _buildHeaderSection(),
      _buildBodySection(),
    ]);
  }

  Widget _buildHeaderSection() {
    return BlocSelector<FeatureBloc, FeatureState, HeaderData>(
      selector: (state) => state.header,
      builder: (context, header) {
        return FeatureHeader(
          data: header,
          onRefresh: () =>
              context.read<FeatureBloc>().add(const FeatureRefreshed()),
        );
      },
    );
  }

  Widget _buildBodySection() {
    return BlocConsumer<FeatureBloc, FeatureState>(
      listener: (context, state) {
        if (state.status == FeatureStatus.failure) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.errorMessage ?? 'Request failed')),
          );
        }
      },
      builder: (context, state) {
        return FeatureBody(
          data: state.sections,
          isLoading: state.status == FeatureStatus.loading,
          onRetry: () =>
              context.read<FeatureBloc>().add(const FeatureRetried()),
          onItemTap: (item) => context
              .read<FeatureBloc>()
              .add(FeatureItemTapped(item: item)),
        );
      },
    );
  }
}
```

推荐做法：

- 页面主结构先用 `_buildPage(children: [...])` 固定下来
- 每个业务区块再在内部接 `BlocBuilder` / `BlocConsumer`
- 让状态消费工具服务于业务区块，而不是反过来控制整页结构

如果 `FeatureView` 的 `build` 已经开始出现长链容器、嵌套滚动、多层列表细节，或者顶层只剩一个巨大的 `BlocConsumer`，就回到 `flutter-no-nesting` 继续拆。

### 3. 副作用和重建分开考虑

- 仅重建 UI：`BlocBuilder`
- 仅副作用：`BlocListener`
- 两者都有：`BlocConsumer`
- 只关心某个字段：`BlocSelector`

不要为了省事一律使用 `BlocConsumer`。

### 4. 事件派发用 `context.read`

推荐：

```dart
onPressed: () => context.read<LoginBloc>().add(const LoginSubmitted())
```

不要在回调里用 `watch`。

## 事件与状态规范

### 1. 事件命名要表达业务动作

推荐：

- `FeatureStarted`
- `FeatureRefreshed`
- `FeatureLoadMoreRequested`
- `LoginSubmitted`
- `ProfileAvatarTapped`

不推荐：

- `DoFeature`
- `ClickButton`
- `GetData`

### 2. 状态设计先选一种风格

常用两种：

- 单状态类 + `status enum`
- 多子类状态

如果大部分字段共享，优先单状态类：

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

### 3. 保证值相等和不可变

状态和事件必须具备稳定的值语义。通常使用：

- `Equatable`
- 或项目已有的等价不可变方案

不要让 state 里塞可变对象然后原地修改。

## Bloc / Cubit 编写规则

### 1. 异步流程必须显式表达状态变化

常见流程：

- `initial`
- `loading`
- `success`
- `failure`

不要让页面在“请求中”和“空数据”之间无法区分。

### 2. 错误状态必须可被 UI 消费

错误至少应提供：

- 用户可展示的信息，或可映射信息
- UI 可判定的失败状态

不要只 `print(e)` 或吞掉异常。

### 3. Bloc 不直接做底层调用

错误：

```dart
final data = await supabase.from('items').select();
```

正确：

```dart
final data = await repository.fetchItems();
```

### 4. 不在 Bloc 中塞 UI 组件概念

不要在 bloc/state/event 中出现：

- `TextEditingController`
- `BuildContext`
- `Color`
- `Widget`

除非项目明确有特殊约束，否则这些都属于 UI 层。

## 测试规范

### 1. Bloc/Cubit 用 `blocTest`

优先使用：

- `package:bloc_test`
- `package:mocktail`

### 2. 至少覆盖这些场景

- 初始状态
- 成功路径
- 失败路径
- 重试或刷新路径
- 关键事件的状态序列

### 3. 示例

```dart
class MockFeatureRepository extends Mock implements FeatureRepository {}

void main() {
  group('FeatureBloc', () {
    late MockFeatureRepository repository;

    setUp(() {
      repository = MockFeatureRepository();
    });

    blocTest<FeatureBloc, FeatureState>(
      'emit [loading, success] when request succeeds',
      build: () {
        when(() => repository.fetchItems()).thenAnswer((_) async => fakeItems);
        return FeatureBloc(repository: repository);
      },
      act: (bloc) => bloc.add(const FeatureStarted()),
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
  });
}
```

## 推荐工作流

当用户要求你实现一个 Flutter BLoC 功能时，按这个顺序执行：

1. 先判断是 `Cubit` 还是 `Bloc`。
2. 定义 view 需要消费的状态，而不是先写 Widget。
3. 设计事件或方法入口。
4. 明确 repository 和 datasource 边界。
5. 写 `Page` 提供 bloc。
6. 写 `View` 消费状态，并按 `flutter-no-nesting` 拆分结构。
7. 写 feature widgets，只传数据和回调。
8. 为 bloc/cubit 写测试。

## 禁忌项

不要这样写：

- 在 `View` 里直接请求接口
- 在 `Page` 里写整页复杂 UI
- 在 `Bloc` 里直接调 SDK
- 一个 `build` 里堆满 `BlocConsumer + Column + Expanded + Padding + List.generate + InkWell`
- 事件名、状态名没有业务语义
- 失败状态没有落到 UI 可消费结构
- 为了用 BLoC 而用 BLoC，简单局部状态也强行上事件流

## 提交前检查

- [ ] 已判断这次该用 `Cubit` 还是 `Bloc`
- [ ] `Page` 只负责提供 bloc，`View` 只负责消费和组织页面
- [ ] view 层结构遵循 `flutter-no-nesting`
- [ ] `Bloc/Cubit` 不直接调用 SDK
- [ ] `Repository` 和 `Datasource` 职责分离
- [ ] 事件和状态命名有明确业务语义
- [ ] 异步流程能区分 loading / success / failure
- [ ] 错误状态能被 UI 正常消费
- [ ] 测试覆盖关键状态流

## 一句话原则

**Bloc 管状态流，Repository 管数据编排，Datasource 管底层调用，View 必须按 no-nesting 组织。**
