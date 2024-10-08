-- local file_path = "/tmp/nvim_trace.json"
local current_file = debug.getinfo(1, "S").source:sub(2)
local package_dir = vim.fn.fnamemodify(current_file, ":p:h:h:h")


local file_watcher
PyTrace = {
    namespace = vim.api.nvim_create_namespace("trace"),
    path = "/tmp/nvim_trace.json",
    highlight = "VirtualPerformance",
    path_to_profiler = package_dir .. "/src/tracer/nvim_py_profile/__main__.py",
    formatter = function(params)
        
    end,

    get_start_command = function (path)
        return PyTrace.path_to_profiler .. " " .. path
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

    setup = function (opts)
        require('nvim-py-profiler.server').start_lua_server()
        opts = opts or {}
        opts.namespace = opts.namespace or vim.api.nvim_create_namespace("trace")
        opts.highlight = opts.highlight or PyTrace.highlight

        self = setmetatable(PyTrace, opts)
        return self
    end
}

PyTrace.__index = PyTrace
return PyTrace
