
-- Import the libuv module
local uv = vim.loop

-- Define your callback function
local function my_callback(str1, num, num1, num2)
    print("Received data:", str1, num, num1, num2)
end

local server = uv.new_tcp()
server:bind("127.0.0.1", 24130)

server:listen(128, function(err)
    assert(not err, err)
    local client = uv.new_tcp()
    server:accept(client)
    client:read_start(
        function(err, data)
            assert(not err, err)
            if data then
            -- Process the received data
            local s = data:gsub("\n", "") -- Remove any newline characters
            -- Parse the tuple from the string
            local str1, num, str2 = string.match(s, "%((.-),%s*(%d+),%s*(.-)%)")
            num = tonumber(num)
            if str1 and num and str2 then
                -- Execute the callback with the parsed data
                my_callback(str1, num, str2)
            else
                print("Failed to parse data:", s)
            end
            else
            client:close()
            end
        end)
    end)

print("Lua TCP server is listening on port 12345")
