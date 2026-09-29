# Controlled Con Artist batch

The contract requires value() == 1. The existing positive-value test is deliberately weak. Three temporary mutations return2,3,4; the proposed stronger assertion checks exactly1. MUTATE_NOTE declares an authorized fixture effect when running value3 inside the helper copy. It is not application behavior.
