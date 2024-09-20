-- local file_path = "/tmp/nvim_trace.json"
local current_file = debug.getinfo(1, "S").source:sub(2)
local package_dir = vim.fn.fnamemodify(current_file, ":p:h:h:h")


local file_watcher
PyTrace = {
    namespace = vim.api.nvim_create_namespace("trace"),
    path = "/tmp/nvim_trace.json",
    highlight = "VirtualPerformance",
    path_to_profiler = package_dir .. "/src/profiler_package/nvim_trace/__main__.py",
    formatter = function(params)
        
    end,

    ---@return table: table with the filenames as keys and a subtable containing the lines and the corresponding times
    read_file = function(path)
        local file = io.open(path, "r")

        if file then
            local content = file:read("*a")
            file:close()

            if content then
                local success, decoded_content = pcall(vim.fn.json_decode, content)
                if success then return decoded_content end
            else
                print("Cannot read trace-file! Ensure paths and formatting is set correctly.")
                return {}
            end
        else
            print("Path to trace file is not readable")
            return {}
        end
    end,

    get_files = function()
        local buffers = vim.api.nvim_list_bufs()
        local files = {}
        for _, bufnr in ipairs(buffers) do
            if vim.api.nvim_buf_is_loaded(bufnr) and vim.api.nvim_buf_get_option(bufnr, 'buflisted') then
                local file_path = vim.api.nvim_buf_get_name(bufnr)
                if file_path ~= "" then files[bufnr] = file_path end
            end
        end
        return files
    end,

    get_subtable = function (path)
        local buf_file_map = PyTrace.get_files()
        print(vim.inspect(buf_file_map))
        local total_table = PyTrace.read_file(path)
        local buffer_time_map = {}

        for buf, file_path in pairs(buf_file_map) do
            for file_name, times in pairs(total_table) do
                if file_name == file_path then
                    buffer_time_map[buf] = {}
                    for line_nr, time in pairs(times) do
                        buffer_time_map[buf][tonumber(line_nr)] = time
                    end
                end
            end
        end
        return buffer_time_map
    end,

    write_text = function()
        local data = PyTrace.get_subtable(PyTrace.path)
        print(vim.inspect(data))

        for buf, subtable in pairs(data) do
            vim.api.nvim_buf_clear_namespace(buf, PyTrace.namespace, 0, -1)

            vim.api.nvim_buf_call(buf, function()
                local max_lines = #vim.api.nvim_buf_get_lines(buf, 0, -1, true)
                for line, trace in pairs(subtable) do
                    if line >= max_lines then break end
                    print(line, trace)
                    vim.api.nvim_buf_set_extmark(buf, PyTrace.namespace, line, 0, {virt_text={{trace, PyTrace.highlight}}, virt_text_pos="right_align", hl_mode="combine"})
                end
            end)
        end
    end,

    watch_file = function (path)
        path = path or "/tmp/nvim_trace.json"
        file_watcher = vim.loop.new_fs_event()
        if not file_watcher then error("Critical filewatcher cannot be started") end
        file_watcher:start(path, {}, vim.schedule_wrap(function()
            PyTrace.write_text()
        end))
    end,

    setup = function (opts)
        require('nvim-py-profiler.server').start_lua_server()
        opts = opts or {}
        opts.namespace = opts.namespace or vim.api.nvim_create_namespace("trace")
        opts.highlight = opts.highlight or PyTrace.highlight
        self = setmetatable(PyTrace, opts)

        PyTrace.watch_file(opts.file or "/tmp/nvim_trace.json")
        return self
    end
}

PyTrace.__index = PyTrace
return PyTrace
