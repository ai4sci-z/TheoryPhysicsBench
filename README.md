# TheoryPhysicsBench

理论物理科研任务的 Harbor 题库，涵盖理论力学、电动力学、统计物理、量子力学、量子场论和广义相对论。

## 下载

| 文件 | 内容 |
| --- | --- |
| [50题交付版](https://github.com/ai4sci-z/TheoryPhysicsBench/releases/download/archive-2026-11-27/TheoryPhysicsBench-50.zip) | 完整任务目录、评分器、参考结果、报告及三轮150条测评记录 |
| [v2开发存档](https://github.com/ai4sci-z/TheoryPhysicsBench/releases/download/archive-2026-11-27/TheoryPhysicsBench-v2-development.zip) | 100项设计登记、30个实际任务目录，含希尔伯特问题与物理任务；制作尚未全部完成 |
| [50题开发源码](https://github.com/ai4sci-z/TheoryPhysicsBench/releases/download/archive-2026-11-27/TheoryPhysicsBench-50-development.zip) | 制作脚本、原型迭代、来源记录和本地运行记录 |
| [单题原型](https://github.com/ai4sci-z/TheoryPhysicsBench/releases/download/archive-2026-11-27/TheoryPhysicsBench-prototypes.zip) | Allen–Dynes 与力学反问题原型 |
| [运行环境](https://github.com/ai4sci-z/TheoryPhysicsBench/releases/download/archive-2026-11-27/TheoryPhysicsBench-infrastructure.zip) | Dockerfile、版本记录、构建与恢复脚本 |

全部文件见 [Releases](https://github.com/ai4sci-z/TheoryPhysicsBench/releases/tag/archive-2026-11-27)。

## 50题版本

| 学科 | 题数 |
| --- | ---: |
| 理论力学 | 5 |
| 电动力学 | 5 |
| 统计物理 | 5 |
| 量子力学 | 5 |
| 量子场论 | 25 |
| 广义相对论 | 5 |

每题包含 `instruction.md`、`task.toml`、`environment/`、`solution/` 和 `tests/`。完整包的顶层为：

```text
group-theoryphysics/
├── benchmark.json
├── tasks/
├── 报告.md
├── results.csv
├── checks/
└── runs/
```

运行记录使用 Harbor 0.24.0、Codex CLI 0.169.0 和 `gpt-6.1-sol`。三轮各50次，平均分分别为0.88、1.00、0.98；单题资源及超时配置保存在 `task.toml` 与原始记录中。

## 开发版本

v2保留了较大规模的设计与制作尝试，包括形式化证明、开放命题、构造题和通用求解器。目录存在不等于已经完成：部分任务只有来源资料，部分仍缺参考运行、完整评分逻辑或环境适配。逐题状态见 `development-status.md`。

源码、未完成实现及必要验证记录一起保留。编译缓存、Python虚拟环境、运行时安装包和Docker镜像二进制未打入存档；构建脚本与版本锁定文件保留在相应目录。部分早期环境使用Linux ARM64，迁移到AMD64时需按锁定版本重建。

## 使用

先下载50题包查看 `benchmark.json` 与逐题题面。`solution/`、`tests/` 用于出题与验收，不应挂载到被测智能体的作答环境。已有程序和文献来源按各自文件中的原始说明保留。
