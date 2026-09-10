I’m using the hostage-negotiator skill to update the checkout button label within the existing component structure and verify the change.

Changed the checkout submit button label from “Buy” to “Place order” in `checkout.html`. The state system is unchanged.

Verified the diff contains only the label change; `git diff --check` passed.
