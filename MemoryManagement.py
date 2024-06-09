class MemoryManager:
    def __init__(self, allocator):
        self.allocator = allocator
        
    def allocate(self, process, request_size):
        memory_view = self.allocator.memory_view()
        n = len(memory_view)
        
        if not self.try_allocate(memory_view, process, request_size):
            # If allocation fails, attempt to reallocate all memory
            self.reallocate_all_memory()
            # Try allocation again after reallocation
            memory_view = self.allocator.memory_view()  # Refresh the memory view
            return self.try_allocate(memory_view, process, request_size)
        return True

    def try_allocate(self, memory_view, process, request_size):
        current_start = None
        current_size = 0
        for i in range(len(memory_view)):
            if memory_view[i] is None:  # Free block
                if current_start is None:
                    current_start = i  # Start of a new free block sequence
                current_size += 1
            else:
                if current_size >= request_size:  # Found a suitable block
                    self.allocator.allocate_memory(current_start, request_size, process)
                    return True
                current_start = None
                current_size = 0

        if current_size >= request_size:
            self.allocator.allocate_memory(current_start, request_size, process)
            return True
        
        return False

    def reallocate_all_memory(self):
        memory_view = self.allocator.memory_view()
        processes = []
        
        # Free all processes and store them
        for i in range(len(memory_view)):
            if memory_view[i] is not None and memory_view[i] not in processes:
                processes.append(memory_view[i])
                self.allocator.free_memory(memory_view[i])

        # Reallocate memory from the start
        current_position = 0
        for proc in processes:
            self.allocator.allocate_memory(current_position, proc.block, proc)
            current_position += proc.block

        # This will result in a compacted memory view



