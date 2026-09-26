# Week 13 companion: recover an unknown effect

This MIT-licensed, synthetic fixture accompanies [The agent timed out after the change went through](https://ericmacdougall.com/journal/the-agent-timed-out-after-the-change-went-through/). It models a fictional inference-service move whose placement request is accepted while the caller loses its reply. No cloud, customer, payment, network or GPU API is called.

`fixture.py` keeps a stable operation ID and an append-only local event list. It separates `EFFECT_UNKNOWN`, `ACCEPTED_PENDING`, `CONVERGED`, `DIVERGED` and `REQUIRES_OWNER`. A missing reply never authorizes a second move. Even an accepted placement is not called complete until placement, account mapping, route and serving readbacks match the intended result. A concurrent version change blocks automatic compensation.

Run the ten owner-labeled examples from this folder with Python 3.11+:

```sh
python -m unittest -v test_fixture.py
```

The negative control deliberately makes `EFFECT_UNKNOWN` authorize a second move. In a disposable shell, set `W13_TEST_MUTANT=1`, rerun the tests and require a failure, then clear the variable. On PowerShell: `$env:W13_TEST_MUTANT='1'; python -m unittest -v test_fixture.py; Remove-Item Env:W13_TEST_MUTANT`. This is a test-only mutation, never a recovery policy.

See [ten bounded probes](ten-probes.md) for experiments on the intended stack. The fixture has no durable storage, authentication, service preconditions, external queue, trace collector, real-time customer probe or protected authorization service. Passing tests establish only these Python branches. They do not establish exactly-once execution or that an agent or orchestration product will preserve correlation in production.

The field note's mechanism references are [AWS Step Functions redrive](https://docs.aws.amazon.com/step-functions/latest/dg/redrive-executions.html), [Temporal Activities](https://docs.temporal.io/activities) and [child workflows](https://docs.temporal.io/child-workflows), [OpenTelemetry messaging spans](https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/), and Microsoft's [compensating transaction pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction). Their product-specific behavior is not exercised by this local fixture.
