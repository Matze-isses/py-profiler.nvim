-- Import the libuv module
local uv = vim.loop
local printer = require('nvim-py-profiler.printer').printer

local function my_callback(str1, num, str2)
    vim.schedule(function() printer(str1, num, str2) end)
end

return {
    define_callback = function(callback)
        my_callback = callback
    end,

    start_lua_server = function ()
        local server = uv.new_tcp()
        server:bind("127.0.0.1", 22122)

        server:listen(128, function(err)
            assert(not err, err)
            local client = uv.new_tcp()
            server:accept(client)
            client:read_start(function(err, data)
                assert(not err, err)
                if data then
                    local s = data:gsub("\n", "")
                    local str1, num, str2 = string.match(s, "%((.-),%s*(%d+),%s*(.-)%)")
                    num = tonumber(num)

                    if str1 and num and str2 then my_callback(str1, num, str2)
                    else print("Failed to parse data:", s) end
                else client:close() end
            end)
        end)

    print("Lua TCP server is listening on port 12345")
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
