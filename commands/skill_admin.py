"""
Admin command to manage the YAML-backed skill registry at runtime.

Usage examples (from in-game as an admin):
  @skills reload
  @skills list
  @skills show <skill_key>
  @skills add <skill_key> label="Label" selectable=true xp_required=120 description="..." [--save]
  @skills update <skill_key> key=value ... [--save]
  @skills remove <skill_key> [--save]
  @skills save

This command is intentionally simple: metadata is set using key=value pairs
(similar to many admin commands). Passing `--save` will attempt to write the
in-memory registry back to `data/skills.yml`.

Locking: Only players with the `Immortals` permission can use this by default;
change the `locks` string to fit your server's permission model.
"""
from evennia import Command
from typeclasses import skills
from evennia.accounts.models import AccountDB

# Permission used to gate this command. Change this constant if you want
# a different admin permission (e.g. 'Developer' or 'builder').
ADMIN_PERMISSION = "Immortals"


def _parse_value(val: str):
    """Parse a string into int/bool/str where reasonable."""
    v = val.strip()
    if not v:
        return v
    # boolean
    if v.lower() in ("true", "yes", "on"):
        return True
    if v.lower() in ("false", "no", "off"):
        return False
    # int
    try:
        return int(v)
    except Exception:
        pass
    # strip surrounding quotes if present
    if (v[0] == v[-1]) and v[0] in ('"', "'"):
        return v[1:-1]
    return v


def _parse_kv_pairs(tokens):
    """Parse tokens of the form key=value into a dict."""
    out = {}
    for token in tokens:
        if "=" not in token:
            continue
        key, val = token.split("=", 1)
        out[key.strip()] = _parse_value(val)
    return out


class CmdSkills(Command):
    """Manage the skills registry.

    See module docstring for usage.
    """
    key = "@skills"
    locks = f"cmd:perm({ADMIN_PERMISSION})"
    help_category = "Admin"

    def func(self):
        if not self.args:
            return self.caller.msg("Usage: @skills reload|list|show|add|update|remove|save ...")
        tokens = self.args.strip().split()
        sub = tokens[0].lower()

        try:
            if sub == "reload":
                skills.reload_skill_registry()
                return self.caller.msg("Skill registry reloaded.")

            if sub == "list":
                keys = skills.get_all_skill_keys()
                if not keys:
                    return self.caller.msg("No skills registered.")
                lines = [f"{k}: {skills.get_skill_meta(k).get('label', '')}" for k in keys]
                return self.caller.msg("\n".join(lines))

            if sub == "show":
                if len(tokens) < 2:
                    return self.caller.msg("Usage: @skills show <skill_key>")
                key = tokens[1]
                meta = skills.get_skill_meta(key)
                if not meta:
                    return self.caller.msg(f"No skill '{key}' found.")
                return self.caller.msg(str(meta))

            if sub in ("add", "update"):
                if len(tokens) < 2:
                    return self.caller.msg(f"Usage: @skills {sub} <skill_key> key=value ... [--save]")
                key = tokens[1]
                tokens_after = tokens[2:]
                write_back = False
                if "--save" in tokens_after:
                    write_back = True
                    tokens_after = [t for t in tokens_after if t != "--save"]
                meta = _parse_kv_pairs(tokens_after)
                # ensure types are correct and set sensible defaults
                if "selectable" in meta:
                    meta["selectable"] = bool(meta["selectable"])
                # register
                skills.register_skill(key, meta, write_back=write_back)
                return self.caller.msg(f"Skill '{key}' registered/updated.{' Saved.' if write_back else ''}")

            if sub == "remove":
                if len(tokens) < 2:
                    return self.caller.msg("Usage: @skills remove <skill_key> [--save]")
                key = tokens[1]
                write_back = "--save" in tokens[2:]
                if key in skills.AVAILABLE_SKILLS:
                    del skills.AVAILABLE_SKILLS[key]
                    if write_back:
                        ok = skills.save_skill_registry()
                        return self.caller.msg(f"Removed '{key}'. Save {'ok' if ok else 'failed'}.")
                    return self.caller.msg(f"Removed '{key}' from registry.")
                return self.caller.msg(f"No skill '{key}' in registry.")

            if sub == "save":
                ok = skills.save_skill_registry()
                return self.caller.msg("Saved." if ok else "Save failed (PyYAML missing or error).")

            # grant/revoke helper for assigning the admin permission to accounts
            if sub == "grantperm":
                if len(tokens) < 2:
                    return self.caller.msg("Usage: @skills grantperm <accountname>")
                acctname = tokens[1]
                acct = AccountDB.objects.filter(db_key__iexact=acctname).first()
                if not acct:
                    return self.caller.msg(f"No account '{acctname}' found.")
                acct.permissions.add(ADMIN_PERMISSION)
                return self.caller.msg(f"Granted {ADMIN_PERMISSION} to {acct.db_key}.")

            if sub == "revokeperm":
                if len(tokens) < 2:
                    return self.caller.msg("Usage: @skills revokeperm <accountname>")
                acctname = tokens[1]
                acct = AccountDB.objects.filter(db_key__iexact=acctname).first()
                if not acct:
                    return self.caller.msg(f"No account '{acctname}' found.")
                acct.permissions.remove(ADMIN_PERMISSION)
                return self.caller.msg(f"Revoked {ADMIN_PERMISSION} from {acct.db_key}.")

            # unknown subcommand
            return self.caller.msg("Unknown subcommand. Usage: @skills reload|list|show|add|update|remove|save ...")

        except Exception as err:
            # keep admin informed but avoid leaking large trace
            return self.caller.msg(f"Error: {err}")
