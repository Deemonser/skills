---
name: flutter-bloc-development
description: Flutter BLoC 状态管理开发规范，涵盖架构分层、设计系统常量、测试标准和命名约定。适用于创建页面、组件、数据集成，或审查/重构 BLoC 相关代码。
allowed-tools: Read Glob Grep
---

# Flutter BLoC 开发规范

基于 BLoC 模式分离业务逻辑与 UI，结合项目设计系统常量，确保代码一致性与可测试性。

---

## 决策树：选择正确的方式

```
用户任务 → 在构建什么？
    │
    ├─ 新页面/功能 → 完整功能实现：
    │   1. 创建功能目录 lib/[feature]/
    │   2. 定义 BLoC（bloc/_event.dart, _state.dart, _bloc.dart）
    │   3. 创建数据层（data/datasources/, repositories/, models/）
    │   4. 构建 UI（view/[feature]_page.dart, view/widgets/）
    │   5. 创建 barrel 文件（[feature].dart, data/data.dart, view/view.dart）
    │
    ├─ 仅新组件 → 表现层：
    │   1. 功能专属：feature/view/widgets/
    │   2. 跨功能复用：shared/widgets/
    │   3. 使用设计系统常量（不允许硬编码）
    │   4. 按需接入已有 BLoC
    │
    ├─ 数据集成 → 数据层：
    │   1. 创建 datasource（feature/data/datasources/）
    │   2. 创建 repository（feature/data/repositories/）
    │   3. 接入现有或新建 BLoC
    │
    ├─ 简单 UI 状态（无复杂事件流）→ 使用 Cubit：
    │   emit(NewState()) 代替 on<Event>
    │
    └─ 重构 → 检查违规项：
        1. 硬编码颜色/间距/字体
        2. 业务逻辑混入 UI
        3. 直接在 repository 调用 SDK
        4. 异步操作前缺少 Loading 状态
        5. Event/State 缺少 Equatable
        6. 错误处理未用 SnackBar + AppColors.error
```

---

## 架构总览

**功能优先结构**（官方 BLoC 推荐）：

```
lib/
├── [feature]/
│   ├── bloc/
│   │   ├── [feature]_bloc.dart
│   │   ├── [feature]_event.dart
│   │   └── [feature]_state.dart
│   ├── data/
│   │   ├── datasources/          # 功能专属 API 调用
│   │   ├── repositories/         # 数据编排
│   │   ├── models/               # 功能专属 DTO
│   │   └── data.dart             # 数据层 barrel 文件
│   ├── view/
│   │   ├── [feature]_page.dart   # Page：提供 BLoC
│   │   ├── [feature]_view.dart   # View：消费 BLoC
│   │   ├── widgets/              # 功能专属组件
│   │   └── view.dart             # View barrel 文件
│   └── [feature].dart            # 功能 barrel 文件
├── shared/
│   ├── data/
│   │   ├── datasources/          # 共享 API 客户端
│   │   ├── models/               # 共享模型（User 等）
│   │   └── data.dart
│   ├── widgets/                  # 跨功能复用组件
│   └── utils/                    # 设计系统（颜色、间距、字体）
└── app.dart
```

### 功能 vs 共享数据选择

| 场景 | 位置 | 示例 |
|------|------|------|
| 仅一个功能使用的 API | `feature/data/` | `EarningsDataSource` |
| 多功能共用的 API 客户端 | `shared/data/` | `ApiClient`, `UserDataSource` |
| 仅一个功能使用的模型 | `feature/data/models/` | `EarningsSummary` |
| 多功能共用的模型 | `shared/data/models/` | `User`, `ApiResponse` |

### Barrel 文件示例

```dart
// earnings/earnings.dart
export 'bloc/earnings_bloc.dart';
export 'bloc/earnings_event.dart';
export 'bloc/earnings_state.dart';
export 'data/data.dart';
export 'view/view.dart';
```

---

## Cubit vs Bloc 选择

| 维度 | Cubit | Bloc |
|------|-------|------|
| API | 方法 → `emit(state)` | 事件 → `on<Event>` → `emit(state)` |
| 复杂度 | 低 | 较高 |
| 可追踪性 | 弱（无事件日志） | 强（事件 + 转换） |
| 适用场景 | 简单状态、UI 驱动逻辑 | 复杂流程、事件驱动、需变换 |

### Cubit 示例

```dart
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);
}
```

### Bloc 示例

```dart
sealed class CounterEvent extends Equatable {
  const CounterEvent();

  @override
  List<Object> get props => [];
}

final class CounterIncrementPressed extends CounterEvent {}
final class CounterDecrementPressed extends CounterEvent {}

class CounterBloc extends Bloc<CounterEvent, int> {
  CounterBloc() : super(0) {
    on<CounterIncrementPressed>((event, emit) => emit(state + 1));
    on<CounterDecrementPressed>((event, emit) => emit(state - 1));
  }
}
```

---

## 命名约定

### 事件命名

**格式：** `BLoC主语` + `名词` + `过去时动词`

| 事件类名 | 含义 |
|----------|------|
| `TodoListSubscriptionRequested` | 订阅 Todo 列表流 |
| `TodoListTodoDeleted` | 删除特定 Todo |
| `LoginFormSubmitted` | 提交登录表单 |
| `ProfilePageRefreshed` | 刷新个人资料页 |

```dart
sealed class TodoListEvent extends Equatable {
  const TodoListEvent();

  @override
  List<Object> get props => [];
}

final class TodoListSubscriptionRequested extends TodoListEvent {}

final class TodoListTodoDeleted extends TodoListEvent {
  const TodoListTodoDeleted({required this.todo});

  final Todo todo;

  @override
  List<Object> get props => [todo];
}
```

### 状态命名

#### 子类方式（各状态携带不同数据）

```dart
sealed class LoginState extends Equatable {
  const LoginState();

  @override
  List<Object> get props => [];
}

final class LoginInitial extends LoginState {}
final class LoginInProgress extends LoginState {}

final class LoginSuccess extends LoginState {
  const LoginSuccess({required this.user});
  final User user;

  @override
  List<Object> get props => [user];
}

final class LoginFailure extends LoginState {
  const LoginFailure({required this.error});
  final String error;

  @override
  List<Object> get props => [error];
}
```

#### 单类方式（所有状态共享相同数据结构）

```dart
enum TodoListStatus { initial, loading, success, failure }

class TodoListState extends Equatable {
  const TodoListState({
    this.status = TodoListStatus.initial,
    this.todos = const [],
    this.error,
  });

  final TodoListStatus status;
  final List<Todo> todos;
  final String? error;

  TodoListState copyWith({
    TodoListStatus? status,
    List<Todo>? todos,
    String? error,
  }) {
    return TodoListState(
      status: status ?? this.status,
      todos: todos ?? this.todos,
      error: error ?? this.error,
    );
  }

  @override
  List<Object?> get props => [status, todos, error];
}
```

---

## BLoC 实现标准

**数据流：**
```
UI 事件 → BLoC (emit Loading) → Repository → Datasource (SDK)
    ↓
响应 → Repository (映射实体) → BLoC (emit Success/Error) → UI
```

**完整 BLoC 示例（含 Loading → Success/Error）：**

```dart
class FeatureBloc extends Bloc<FeatureEvent, FeatureState> {
  final FeatureRepository _repository;

  FeatureBloc({required FeatureRepository repository})
      : _repository = repository,
        super(FeatureInitial()) {
    on<FeatureActionRequested>(_onActionRequested);
  }

  Future<void> _onActionRequested(
    FeatureActionRequested event,
    Emitter<FeatureState> emit,
  ) async {
    emit(FeatureLoading());
    try {
      final result = await _repository.doSomething(event.param);
      emit(FeatureSuccess(result));
    } catch (e) {
      emit(FeatureError(e.toString()));
    }
  }
}
```

**重要**：异步操作前必须先 emit Loading，绝不跳过。

---

## 数据层

**Datasource** — 仅做 SDK 调用：

```dart
class FeatureDataSource {
  final SupabaseClient _supabase;
  FeatureDataSource(this._supabase);

  Future<Map<String, dynamic>> fetch() async {
    return await _supabase.from('table').select().single();
  }
}
```

**Repository** — 编排与映射，不直接调用 SDK：

```dart
class FeatureRepository {
  final FeatureDataSource _dataSource;
  FeatureRepository(this._dataSource);

  Future<DomainEntity> fetchData() async {
    final response = await _dataSource.fetch();
    return DomainEntity.fromJson(response);
  }
}
```

---

## 设计系统（不可硬编码）

### 颜色
✅ `AppColors.primary`、`AppColors.error`、`AppColors.textPrimary`
❌ `Color(0xFF...)`、`Colors.blue`、内联 hex 值

### 间距
✅ `AppSpacing.xs`(4)、`AppSpacing.sm`(8)、`AppSpacing.md`(16)、`AppSpacing.lg`(24)、`AppSpacing.xl`(32)
✅ `AppSpacing.screenHorizontal`(24)、`AppSpacing.screenVertical`(16)
❌ `EdgeInsets.all(16.0)`、硬编码 padding

### 圆角
✅ `AppRadius.sm`(8)、`AppRadius.md`(12)、`AppRadius.lg`(16)、`AppRadius.xl`(24)
❌ `BorderRadius.circular(12)`、内联圆角值

### 字体
✅ `AppTypography.headlineLarge`、`AppTypography.bodyMedium`、`theme.textTheme.bodyMedium`
❌ `TextStyle(fontSize: 16)`、内联文字样式

---

## UI 模式

### Page / View 分离（强制）

- **Page**：通过 `BlocProvider` 创建并提供 BLoC，不包含 UI 逻辑
- **View**：通过 `BlocBuilder`/`BlocConsumer` 消费状态，不创建 BLoC

```dart
// feature_page.dart — 提供 BLoC
class FeaturePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => FeatureBloc(repository: context.read()),
      child: const FeatureView(),
    );
  }
}

// feature_view.dart — 消费 BLoC
class FeatureView extends StatelessWidget {
  const FeatureView({super.key});

  @override
  Widget build(BuildContext context) {
    return GradientScaffold(
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(AppSpacing.screenHorizontal),
              child: HeaderWidget(),
            ),
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.screenHorizontal,
                ),
                child: BlocConsumer<FeatureBloc, FeatureState>(
                  listener: (context, state) {
                    if (state is FeatureError) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text(state.message),
                          backgroundColor: AppColors.error,
                        ),
                      );
                    }
                  },
                  builder: (context, state) {
                    if (state is FeatureLoading) {
                      return const Center(child: CircularProgressIndicator());
                    }
                    if (state is FeatureSuccess) {
                      return SuccessWidget(data: state.data);
                    }
                    return const SizedBox.shrink();
                  },
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(AppSpacing.screenHorizontal),
              child: ActionButton(
                onPressed: () =>
                    context.read<FeatureBloc>().add(const ActionEvent()),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

### context.read vs context.watch

| 用法 | 场景 |
|------|------|
| `context.read<Bloc>().add(Event())` | 回调中派发事件（`onPressed`、`onTap`） |
| `context.watch<Bloc>().state` | `build` 方法中监听状态 |
| `BlocBuilder` | 仅需重建 UI |
| `BlocListener` | 仅需副作用（导航、SnackBar） |
| `BlocConsumer` | 同时需要重建 + 副作用 |
| `BlocSelector` | 仅监听状态的某个字段变化 |

**禁止**在 `build` 方法之外使用 `context.watch`。

---

## 测试规范

- **使用 `blocTest()`**（`package:bloc_test`）测试所有 Bloc 和 Cubit，禁止用原始 `test()` + 手动 stream 断言
- **使用 `package:mocktail` 进行 mock**，禁止 `package:mockito`
- 测试文件镜像功能目录结构，放在 `test/` 下

### Cubit 测试示例

```dart
group('CounterCubit', () {
  late CounterCubit cubit;

  setUp(() => cubit = CounterCubit());
  tearDown(() => cubit.close());

  test('初始状态为 0', () => expect(cubit.state, 0));

  blocTest<CounterCubit, int>(
    'increment 后 emit 1',
    build: () => CounterCubit(),
    act: (cubit) => cubit.increment(),
    expect: () => [1],
  );
});
```

### Bloc 测试示例

```dart
class MockFeatureRepository extends Mock implements FeatureRepository {}

group('FeatureBloc', () {
  late MockFeatureRepository repository;
  late FeatureBloc bloc;

  setUp(() {
    repository = MockFeatureRepository();
    bloc = FeatureBloc(repository: repository);
  });

  tearDown(() => bloc.close());

  blocTest<FeatureBloc, FeatureState>(
    '请求成功时 emit [Loading, Success]',
    build: () {
      when(() => repository.fetchData()).thenAnswer((_) async => fakeData);
      return FeatureBloc(repository: repository);
    },
    act: (bloc) => bloc.add(const FeatureActionRequested()),
    expect: () => [isA<FeatureLoading>(), isA<FeatureSuccess>()],
  );
});
```

---

## 核心规则（一票否决）

| 规则 | 正确 | 错误 |
|------|------|------|
| 异步前 emit Loading | ✅ 必须 | ❌ 跳过 Loading |
| 业务逻辑位置 | ✅ BLoC/Cubit | ❌ Widget/Page |
| SDK 调用位置 | ✅ Datasource | ❌ Repository 直接调用 |
| BLoC 间通信 | ✅ 通过 UI 或共享 Repository | ❌ BLoC 直接依赖另一个 BLoC |
| 颜色/间距/字体 | ✅ 设计系统常量 | ❌ 硬编码值 |
| 错误提示 | ✅ SnackBar + AppColors.error | ❌ print / 忽略 |
| Event/State 相等性 | ✅ Equatable | ❌ 不实现 |
| 测试 mock | ✅ mocktail | ❌ mockito |

---

## 提交前检查清单

- [ ] Event/State/BLoC 使用 `Equatable`（或 sealed class）
- [ ] 所有异步操作：Loading → Success/Error
- [ ] UI 中无业务逻辑
- [ ] Datasource 之外无 SDK 直接调用
- [ ] 零硬编码颜色/间距/字体
- [ ] 错误处理使用 SnackBar + `AppColors.error`
- [ ] 使用 `blocTest()` 编写测试，mock 用 `mocktail`
- [ ] Page 提供 BLoC，View 消费 BLoC
- [ ] 代码已通过 `dart format`
