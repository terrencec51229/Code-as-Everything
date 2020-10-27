:::info
###### tags: `Internal` `Automation` `Ansible`
:::

# Site Down Procedure for The Maintenance

## The driver

Although there are just a few interfaces and devices that need to be turned off or offline before the maintenance window, however, it has been taken place routinely (every two months). Meanwhile, because of the cloud strategy, there are more and more hybrid-cloud services have been launched as well. In other words, there are more and more changes required before the maintenance window, too.

As a result, that is why we aim to simplify the entire site down procedures that recorded on the [Confluence Page](https://bigasia.atlassian.net/wiki/spaces/RCIC/pages/138513193/Site+down+procedure+for+the+maintenance) via Ansible.

## The structure of the playbooks

There are two tiers of the entire playbooks.
* The top-level are *siteoff.yml* and *siteon.yml*. What they do is to **import** all the required playbooks, therefore, we do not need to execute each playbook accordingly.
* The bottom-level are *Cisco-DisableExtTrunk* and *F5-DisableFailsafe*. All the required actions are tasks are encoded under those folders.
* Some of the shared resources that would be re-used by all the playbooks, such as credentials and inventory, that are defined in *Shared-Resources*.
