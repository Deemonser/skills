---
name: test-spec-first
description: 用于编写、重构或补全测试文件。仅在用户明确要求实际新增或修改测试代码时使用。强制要求先创建只包含测试函数名和 `Scenario / Given / When / Then` 注释的空测试骨架文件，并在继续实现前向用户确认。未完成骨架并获得确认前，禁止编写任何正式测试代码。
version: 2.0.0
---

# Test Spec First

## 规则

- 先写 BDD 骨架，再写正式测试代码
- BDD 骨架必须把 `Scenario / Given / When / Then` 写在测试函数前
- 写完骨架后，必须先向用户确认是否继续
- 在用户确认前，禁止写断言、mock、fixture、helper、测试数据或任何正式测试实现

## 什么时候用

- 用户明确要求新增测试
- 用户明确要求修改或补全测试
- 用户明确要求补测试覆盖、补回归测试、补单元测试、补集成测试、补 widget 测试

不要用于：

- 闲聊
- 纯概念讨论
- 未进入测试实现阶段的方案交流

## 执行顺序

1. 先找项目内同层级测试文件，沿用命名和注释风格
2. 创建只含测试名和 `Scenario / Given / When / Then` 注释的空测试文件
3. 向用户确认是否继续
4. 用户确认后，再补正式测试实现

## 骨架文件允许内容

- 文件导入
- `group`
- 空测试函数
- `Scenario / Given / When / Then` 注释

确认前禁止：

- `expect`
- mock / fixture / helper
- act / arrange / verify
- 真实测试数据
- 任何正式测试逻辑

## 注释格式

BDD 用例描述要作为**测试函数前的注释**。

```dart
// HE-001
// Scenario: 恢复 1 点生命
// Given 我方单位生命值 2，最大生命值 6
// When 使用治疗卡
// Then 生命值恢复 1 点
test('restores one life when using heal card', () {
});
```

```gdscript
## HE-001
## Scenario: 恢复1点生命
## Given 我方单位生命值2，最大生命值6
## When 使用治疗卡
## Then 生命值恢复1点
func test_heal_basic() -> void:
    pass
```

要求：

- 每个测试前都必须有完整的 `Scenario / Given / When / Then`
- `Given / When / Then` 只写行为，不写实现细节
- 测试名和注释必须表达行为

## 用户确认

完成骨架后，必须先询问用户是否继续。

优先使用 `AskUserQuestion`。如果当前环境没有这个工具，就直接在对话里询问，并停止继续实现。

## 确认后

用户确认后，才允许补正式测试代码。此时可以在测试函数内部继续使用：

- `准备`
- `执行`
- `验证`

## 禁忌项

- 未写行为骨架就直接写测试实现
- 未确认就直接补 assert / mock / fixture
- 把 `Scenario / Given / When / Then` 写成技术细节清单
- 一次性把整份测试文件写满，不给用户审阅行为层机会

## 一句话原则

**先写带 `Scenario / Given / When / Then` 注释的空测试骨架，先确认，再写正式测试代码。**
