let s:current_script = expand('<sfile>')
let s:absolute_path = fnamemodify(s:current_script, ':p')
let g:nvim_py_profiler_path = fnamemodify(s:absolute_path, ':h:h')
