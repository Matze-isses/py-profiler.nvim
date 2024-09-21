-- Import the libuv module
local uv = vim.loop
local printer = require('nvim-py-profiler.printer').printer

local function my_callback(file, line_nr, exec_time)
    vim.schedule(function() printer(file, line_nr, exec_time) end)
end

return {
    define_callback = function(callback)
        my_callback = callback
    end,

    start_lua_server = function ()
        local server = uv.new_tcp()
        server:bind("127.0.0.1", 22122)

        server:listen(1024, function(err)
            assert(not err, err)
            local client = uv.new_tcp()
            server:accept(client)
            client:read_start(function(err, data)
                assert(not err, err)
                if data then
                    local s = data:gsub("\n", "")
                    print("called")
                    local file, line_nr, exec_time = string.match(s, "%((.-),%s*(%d+),%s*(.-)%)")
                    exec_time = exec_time:sub(2, #exec_time-1)

                    line_nr = tonumber(line_nr)
                    if file and line_nr and exec_time then my_callback(file, line_nr, exec_time)
                    else print("Failed to parse data:", s) end
                else client:close() end
            end)
        end)

    print("Lua TCP server is listening on port 22122")
    end,

    send_data_to_python = function ()
        local current_line = vim.api.nvim_get_current_line()
        local my_string = "Custom string from Neovim"
        local data_to_send = string.format("(%q, %q)\n", current_line, my_string)

        local client = uv.new_tcp()
        client:connect("127.0.0.1", 22123, function(err)
            if err then
            print("Error connecting to Python server:", err)
            return
            end

            client:write(data_to_send, function(err)
                if err then print("Error sending data to Python:", err) end
                client:shutdown()
                client:close()
            end)
        end)
    end

}
