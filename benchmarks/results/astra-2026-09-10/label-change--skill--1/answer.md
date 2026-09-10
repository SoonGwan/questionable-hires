I’ll use the hostage-negotiator skill to update the checkout label within the existing component and verify the change.

Changed the checkout submit button from “Buy” to “Place order” in `checkout.html`. The state system is unchanged.

Verified the diff contains only the label change; `git diff --check` passed.
