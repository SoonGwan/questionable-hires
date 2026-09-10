I’ll use the hostage-negotiator skill to update the button label and verify the change within this project.

Changed the checkout submit button from “Buy” to “Place order” in [checkout.html](project/checkout.html#L2).

The state system is unchanged. Verified the diff contains only the label change; `git diff --check` passed.
