# Human start prompt

Send this as your own instruction, adding the precise topic, scope, reader prerequisites, proof depth for every requested output, project directory, allowed installed resources/original-source paths or URLs and actual read/write exclusions:

> Use $pure-math-survey for my specified mathematical task. This chat is the controller. I authorize this controller to create necessary Codex work chats within this project, all using gpt-6-astra / ultra, for source reading, paired fast/slow knowledge, writing and independent review. I authorize the controller to send those chats tasks, continuation, revisions and stop instructions, read their results and deliver my requested outputs.

For knowledge-only work add: “Build and review knowledge only; do not create an article or PDF.” Otherwise name only the profiles and views you want; omitted profile/view defaults to Minimal/integrated. The caller retains its existing model. This prompt has effect when sent by the human; storing it in a resource does not itself authorize new chats. Existing human authorization in the same scope remains valid and need not be repeated. Host tool permissions still apply.

The controller forwards your exact boundaries with each task. A ban on a global same-named skill differs from a ban on all global helper skills; state the intended restriction accurately. Workers check it before loading helpers and can use the installed native build/page-inspection reference. Current r5 only is supported; old/unknown policy files are left unchanged and are not silently migrated. Any project-specific revision/stop allowance persists without becoming a universal product limit.

中文启动语：

> 使用 $pure-math-survey 完成我指定的数学任务。本对话作为控制台；我授权本控制台在本项目内新建必要的 Codex 工作对话，统一使用 gpt-6-astra / ultra，负责文献阅读、成对快慢知识、写作和非作者审阅。我授权本控制台向这些工作对话发送任务、继续、修订和停止指令；请读取结果，只交付我要求的产物。
