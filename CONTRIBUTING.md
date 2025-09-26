## Contributing

1. Create a feature branch from `develop`.
2. Run `make policy.test` and `make tf.plan ENV=dev` before pushing.
3. Format and validate infra: `make tf.fmt ENV=dev && make tf.validate ENV=dev`.
4. Run tests and linters: `make test.bot && make lint.py && make type.py`.
3. Include Impact Brief in PR description; link artifacts.
4. Squash merge to `develop`; promotion via GitOps.


