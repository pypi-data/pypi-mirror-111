Highlights:
   - **Automatic differentiation**
      - Automatically determine AdStack's size (#2438) (by **xumingkuan**)
   - **Language and syntax**
      - Fix parameter conflict between ti.maybe_transform_ti_func_call_to_stmt() and ti.external_func_call() (#2470) (by **squarefk**)
   - **Metal backend**
      - Support pointer SNode on Metal (#2441) (by **Ye Kuang**)

Full changelog:
   - [ci] Fix docker prebuilt binary link (#2483) (by **Ye Kuang**)
   - [wasm] Implement materialize() for wasm backend and clean up unused functions (#2480) (by **squarefk**)
   - [misc] Unify std::filesystem header (#2478) (by **Ye Kuang**)
   - [opengl] Dump compute shader source code when print_kernel_llvm_ir is true (#2479) (by **xndcn**)
   - [metal] Fix randseedoffset_in_runtime_buffer (#2477) (by **Ye Kuang**)
   - [Metal] Support pointer SNode on Metal (#2441) (by **Ye Kuang**)
   - [wasm] Recover code (#2476) (by **ljcc0930**)
   - [AutoDiff] Automatically determine AdStack's size (#2438) (by **xumingkuan**)
   - [misc] Add checking of gitpython in cmake (#2473) (by **xndcn**)
   - [ci] Restrict slash-command-dispatch to PR only (#2472) (by **Ye Kuang**)
   - [ir] Use SNodeTree to implement root (#2449) (by **Ye Kuang**)
   - [Lang] Fix parameter conflict between ti.maybe_transform_ti_func_call_to_stmt() and ti.external_func_call() (#2470) (by **squarefk**)
