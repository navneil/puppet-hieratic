# == Class: hieratic
#
# Internal class- this should be called through Hieratic, not directly.
#
# === Authors
#
# Robert Hafner <tedivm@tedivm.com>
#
# === Copyright
#
# Copyright 2015 Robert Hafner
#

class hieratic::firewall (
  $global_enable = true,
  $firewall_label = firewall,
  $firewall_enabled = false,
  $firewall_defaults = {},
  $firewall_pre_label = firewall_pre,
  $firewall_pre_enabled = false,
  $firewall_pre_defaults = {},
  $firewall_post_label = firewall_post,
  $firewall_post_enabled = false,
  $firewall_post_defaults = {},
) {

  if(defined('firewall')
    and ($firewall_enabled or $global_enable)) {

    resources { 'firewall':
      purge => true
    }

    Firewall {
      before  => Class['hieratic::firewall::post'],
      require => Class['hieratic::firewall::pre'],
    }

    $firewall_config = hiera_hash($firewall_label, {})
    create_resources(firewall, $firewall_config, $firewall_defaults)

    class { ['hieratic::firewall::pre', 'hieratic::firewall::post']: }
  }
}
