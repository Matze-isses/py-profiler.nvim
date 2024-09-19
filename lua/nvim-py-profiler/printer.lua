
local function get_bufid_by_path_if_visible(path)
  for _, win in ipairs(vim.api.nvim_list_wins()) do
    local buf = vim.api.nvim_win_get_buf(win)
    local buf_name = vim.api.nvim_buf_get_name(buf)
    if buf_name == path then
      return buf
    end
  end
  return nil
end

local function print_line(path, line, text)
    local buf = get_bufid_by_path_if_visible(path)
    if not buf then return end

    vim.api.nvim_buf_clear_namespace(buf, PyTrace.namespace, 0, -1)

    vim.schedule(function()
        vim.api.nvim_buf_call(buf, function()
            local max_lines = #vim.api.nvim_buf_get_lines(buf, 0, -1, true)
            if line >= max_lines then return end
            vim.api.nvim_buf_set_extmark(buf, PyTrace.namespace, line, 0, {virt_text={{text, PyTrace.highlight}}, virt_text_pos="right_align", hl_mode="combine"})
        end)
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
