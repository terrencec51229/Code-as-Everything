:::info
###### tags: `Internal` `Automation` `Ansible`
:::

<style>
.fontColor {
  color: #FF5733;
}
.fontColor2 {
  color: #CC66FF;
}
.fontColorH2 {
  color: #FFBD33
}
.fontColorH3{
  color: #FF338A
}
.fontFace {
  font-weight: Bold;
  font-style: Italic;
}
</style>

[TOC]

# Site Down Procedure for The Maintenance

## <span class="fontColorH2">The driver</span>

Although there are just a few interfaces and devices that need to be turned off or offline before the maintenance window, however, it has been taken place routinely (every two months). Meanwhile, because of the cloud strategy, there are more and more hybrid-cloud services have been launched as well. In other words, there are more and more changes required before the maintenance window, too.

As a result, that is why we aim to simplify the entire site down procedures that recorded on the [Confluence Page](https://bigasia.atlassian.net/wiki/spaces/RCIC/pages/138513193/Site+down+procedure+for+the+maintenance) via Ansible.

## <span class="fontColorH2">The structure of the playbooks </span>

There are two tiers of the entire playbooks.
* The top-level are <span class=fontColor>siteoff.yml</span> and <span class=fontColor>siteon.yml</span>. What they do is to <b>import</b> all the required playbooks, therefore, we do not need to execute each playbook accordingly.
* The bottom-level are <span class=fontColor>Cisco-DisableExtTrunk</span> and <span class=fontColor>F5-DisableFailsafe</span>. All the required actions are tasks are encoded here.
* Some of the shared resources that would be re-used by all the playbooks, such as credentials and inventory, that are defined in <span class=fontColor>Shared-Resources</span>.
