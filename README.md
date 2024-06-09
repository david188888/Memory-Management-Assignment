# Memory-Management-Assignment
It is an assignment for OS lecture about Memory-Management


## 概述
本模块提供了一个内存管理系统，通过 `MemoryManager` 类来处理内存的分配和释放。该类使用一个分配器对象来具体执行内存操作。

## 类和方法

### `MemoryManager` 类

#### 构造函数
- `__init__(self, allocator)`
  - 参数 `allocator`：负责具体的内存分配和释放的对象。
  - 该构造函数初始化一个 `MemoryManager` 实例，存储传入的分配器以供后续使用。

#### `allocate` 方法
- `allocate(self, process, request_size)`
  - 参数 `process`：请求内存的进程。
  - 参数 `request_size`：请求的内存大小（以单位为计）。
  - 此方法尝试为指定进程分配所需大小的内存。如果初始分配尝试失败，将触发全部内存的重新分配流程，并再次尝试分配。

#### `try_allocate` 方法
- `try_allocate(self, memory_view, process, request_size)`
  - 参数 `memory_view`：当前内存状态的快照，表示哪些内存块是被占用的，哪些是空闲的。
  - 此方法检查是否有足够的连续空闲块来满足请求，如果有，则分配内存给指定进程并返回 `True`，否则返回 `False`。

#### `reallocate_all_memory` 方法
- `reallocate_all_memory(self)`
  - 此方法释放所有内存块，然后按照一定顺序重新分配，以达到内存压缩的目的。

## 工作流程
1. 当请求分配内存时，`allocate` 首先尝试通过 `try_allocate` 来分配内存。
2. 如果初始尝试失败，则调用 `reallocate_all_memory` 来压缩内存并重新尝试分配。
3. `try_allocate` 方法遍历内存视图，寻找足够大的空闲区块来满足分配请求。
4. 如果找到合适的空闲区块，通过 `allocator` 的方法将内存分配给进程。
5. 如果在整个内存中找不到足够的空间，则分配失败。

## 模块的用途
此模块适用于需要精细控制内存分配的场景，如操作系统、模拟器或其他需要管理内存的应用。
