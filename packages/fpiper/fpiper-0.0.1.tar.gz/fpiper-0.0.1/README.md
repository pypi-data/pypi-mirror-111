When coming from a functional background, it is normal to miss common
_chainable_ combinators for container types, namely:

- `map`|`fmap`
- `filter`|`where`
- `flatMap`|`bind`|`collect`

This library contains simple wrappers for `Optional` and `Iterable` Python
values which provide just that.

The library is currently in very experimental stage, use at your own risk.

An example:

```
  from fpiper import pipe, pipeOpt

  x = pipe(myList).filter(lambda x: x > 0).flatMap(lambda x: x*2).run()
  y = pipeOpt(loadCustomer).flatMap(validateCustomer).map(submitCustomer).run()
```

