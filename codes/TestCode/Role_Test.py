
from RoleModule.role import Role
from RoleModule.player_role import PlayerRole
from RoleModule.enemy_role import EnemyRole
from RoleModule.npc_role import NPCRole

role = EnemyRole(name = "actor1", modelId = "sound123123")
role.print_all_attr()

print role.get_all_attr()

role.set_attr_value("asd", 123)
role.set_attr_value("name", "asdasdasdasd")

role.append_role_attr("name", "zxc")
print "asdlasldjalsdka:", role.get_attr_value("ableToAtck")

def foo():
    pass

role.bind_input_to_action("event", foo)

print role.get_attr_value("modelId")

role.print_all_attr()

