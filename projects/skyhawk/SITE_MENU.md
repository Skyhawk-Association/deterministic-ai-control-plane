# Site Menu Reference (skyhawk.org)

**Canonical copy:** this file (`projects/skyhawk/SITE_MENU.md`, public DACP repository). Drupal node 49457 points here.

**Migrated** 2026-09-27 from Drupal node 49457 revision 67898. Sanitized for publication: 0 server address(es) and 0 email address(es) removed. Otherwise verbatim.

---

## Confirmed Facts

- There is no menu literally named "Blade" — Blade is a top-level link inside the main navigation menu (machine name: main), alongside Association, The A-4, Hot Rod, Attack, Units.

- Blade parent link: title "Blade", ID 83, UUID 2d057b5a-dff5-4973-9d9c-b3e6fea4e2b8. (ID 82, "Blade's LOST-D", is a sibling/child item, not the parent.)

- Menus that exist on this site: account, admin, devel, footer, main, tools.

## How to Add a Menu Link Under Blade

\Drupal\menu_link_content\Entity\MenuLinkContent::create([
'title' => 'Your Title',
'link' => ['uri' => 'internal:/your/path'],
'menu_name' => 'main',
'parent' => 'menu_link_content:2d057b5a-dff5-4973-9d9c-b3e6fea4e2b8',
'weight' => 0,
'enabled' => TRUE,
])->save();

### Ready Room Reunion Navigation

- Association > Reunions remains the public-facing Reunion destination.

- Ready Room > My Reunion Events is the established authenticated Reunion-management and recovery destination.

- Ready Room > Request a Reunion is the authenticated entry point for a new Reunion request.

- The temporary duplicate Ready Room > My Reunions entry is retired. Do not recreate another menu link to duplicate the established My Reunion Events function.

- Keeper instructional email must explain public versus management navigation so the email is useful but is never the only recovery path.
