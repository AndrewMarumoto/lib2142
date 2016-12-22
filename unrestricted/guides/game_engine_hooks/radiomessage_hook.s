; save register state
push rdi
push rsi
push rdx
push rbx
push rbp
push r12
push r13
push r14

; save pointer to the RadioMessageReceivedEvent instance so it can be accessed by python
lea rax, [rip]
and rax, -0x1000
mov [rax+0xf00], rsi

; get our python command into rdi as the argument for PyRun_SimpleString
lea rdi, [rip+cmd]

; call PyRun_SimpleString
mov rax, 0x407d60
call rax

; restore register state
pop r14
pop r13
pop r12
pop rbp
pop rbx
pop rdx
pop rsi
pop rdi

; run the instructions that were overwritten with our jmp
mov [rsp-0x20], rbp
mov [rsp-0x18], r12
mov rbp, rsi

; jump back into the hooked function
mov rax, 0x45762D
jmp rax

cmd:


