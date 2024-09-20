

# Early development state!
Usage at own risk! 
The times for execution do not match the real once due to inconsistencies of the python setprofile functionality. 
If there are better possibilities to integrate contact me or do a pull request.

# Structure
```mermaid
flowchart TB
    subgraph skript
        line1(Line)
        line2(Line)
        line3(Line)
        line4(...)
    end
    profiler(Inbuild Python Profiler)
    tracer(Inbuild Python Tracer)
    server_python(TCP\nPython)
    server_lua(TCP\nLua Api)
    buf(Neovim Buffer)
    tracer --attached to the execution--> skript
    line1 --raises line event-->tracer
    tracer --reacts in subthread,\n whenever new line is entered-->profiler
    profiler --time of execution-->server_python
    server_python --> server_lua
    server_lua --After filtering and sorting--> buf 
```

