# Authority map for one agent route

Copy this for each host, delegated agent, browser or desktop tool, and external provider route. Fill it from an observed run, not a product label.

| Boundary | Evidence to record |
| --- | --- |
| Proposed action | Exact caller, tool, arguments, task and policy version |
| Interception point | Hook/wrapper/service method actually reached in a harmless trial |
| Deny behavior | Return code, worker-visible result, retry/fallback route |
| Bypass search | Delegation, shell, API, browser, background or resumed-session route |
| Final authority | Identity/permission checked immediately before side effect |
| Independent readback | Service or filesystem state observed outside the worker summary |
| Drift trigger | Tool registry, policy, credential, model or permission version change |
| Owner | Person who sets expected behavior and accepts residual risk |

One green hook unit test is evidence for that script, not every route. Deliberately attempt a safe forbidden operation through each route and prove the side effect did not occur. Record unknown routes as unknown rather than covered.
