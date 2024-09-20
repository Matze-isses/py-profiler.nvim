
---@param path string: path at which it should be printed. Not checked within this method if the path is correct! However, it is checked if the buffer is visible.
---@param line number: line number at which the text should be printed
---@param text string: text to print
local function print_line(path, line, text)
    path = path:sub(2, #path-1)
    local win_list = vim.api.nvim_list_wins()
    local buffers = {}

    for _, win in ipairs(win_list) do
        local buf = vim.api.nvim_win_get_buf(win)
        local buf_name = vim.api.nvim_buf_get_name(buf)
        print(path, buf_name)
        print(path:match(buf_name))
        print(buf_name:match(path))
        if buf_name == path then
            buffers[#buffers+1] = buf
            print(path, buf_name)
        end
    end
    print(#buffers)

    vim.schedule(function()
        for _, buf in pairs(buffers) do
            if not buf then return end
            vim.api.nvim_buf_clear_namespace(buf, PyTrace.namespace, line-1, line)

            vim.api.nvim_buf_call(buf, function()
                local max_lines = #vim.api.nvim_buf_get_lines(buf, 0, -1, true)
                if line >= max_lines then return end
                vim.api.nvim_buf_set_extmark(buf, PyTrace.namespace, line-1, 0, {virt_text={{text, PyTrace.highlight}}, virt_text_pos="right_align", hl_mode="combine"})
            end)
        end
    end)
end


local function test_function()
    local current_buf = vim.api.nvim_get_current_buf()
    local current_buf_name = vim.api.nvim_buf_get_name(current_buf)
    print_line(current_buf_name, 5, "Test")
end

return {
    ---@param path string: path at which it should be printed. Not checked within this method if the path is correct! However, it is checked if the buffer is visible.
    ---@param line number: line number at which the text should be printed
    ---@param text string: text to print
    printer = function(path, line, text) print_line(path, line, text) end,
}
