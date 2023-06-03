import os
import jinja2
import json
import argparse

args = None

TYPE_CHOICES = ['stairs', 'wall', 'slab']
BLOCK_CHOICES=["concrete", "terracotta" , "glazed_terracotta"]
COLOR_CHOICES = ["white", "orange", "magenta" , "light_blue" , "yellow",
                 "lime", "pink" , "gray" , "light_gray", "cyan", "purple" ,
                 "blue" , "brown" , "green", "red" , "black"]



SCRIPT_PATH = os.path.abspath(__file__)
RESOURCE_PATH = f"{SCRIPT_PATH}\..\..\src\main\\resources"
ASSETS_PATH = f"{RESOURCE_PATH}\\assets\\terraconcretia"
DATA_PATH = f"{RESOURCE_PATH}\\data"

GENERAL_TEMPLATES_PATH= f"{SCRIPT_PATH}\\..\\templates\general"
SLAB_TEMPLATES_PATH = f"{SCRIPT_PATH}\\..\\templates\\slabs"
WALL_TEMPLATES_PATH = f"{SCRIPT_PATH}\\..\\templates\\walls"

BLOCKSTATES_PATH=f"{ASSETS_PATH}\\blockstates"
MODELS_BLOCK_PATH=f"{ASSETS_PATH}\\models\\block"
MODELS_ITEM_PATH=f"{ASSETS_PATH}\\models\\item"
LOOT_TABLE_PATH = f"{DATA_PATH}\\terraconcretia\loot_tables\\blocks"
RECIPES_PATH = f"{DATA_PATH}\\terraconcretia\\recipes"

EN_US_LANG_JSON_PATH=f"{ASSETS_PATH}\lang\en_us.json"
PICKAXE_PATH = f"{DATA_PATH}\\minecraft\\tags\\blocks\\mineable\\pickaxe.json"
WALL_JSON_PATH = f"{DATA_PATH}\\minecraft\\tags\\blocks\\walls.json"

def verb_print(string):
    if args.verbose:
        print(string)

def add_kv_pair_to_json(file_path, key_value_string):
    # Read the JSON file
    # print(key_value_string)
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    # Split the key-value string into key and value
    key, value = key_value_string.split(':', 1)

    value = value.replace("_" , " ")
    # Add the new key-value pair to the JSON
    json_data[key.lower().strip().replace("\"","")] = value.strip().replace("\"","")

    # Write the updated JSON back to the file
    if args.dryrun:
        print("dryrun, not modifying anything")
    else:
        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=4)

def add_value_to_json(file_path, value):
    # Read the JSON file    
    value = value.replace("\"","")

    with open(file_path, 'r') as file:
        json_data = json.load(file)
    # Add the value to the "values" array
    if value in json_data['values']:
        return
    json_data["values"].append(value)
    json_data["values"].sort()

    # Write the updated JSON back to the file
    if args.dryrun:
        print("dryrun, not modifying anything")
    else:
        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=4)


def generate_lang_string(color,block,type):
    with open(f"{SCRIPT_PATH}\\..\\templates\\general\\lang.j2") as file:
        template_content = file.read()
    template = jinja2.Template(template_content)

    rendered_content = template.render(color=color.title(), block=block.title(),type=type.title())
    verb_print(rendered_content)
    return rendered_content

def generate_pickaxe_string(color,block,type):
    with open(f"{SCRIPT_PATH}\\..\\templates\\general\\pickaxe.j2") as file:
        template_content = file.read()
    template = jinja2.Template(template_content)

    rendered_content = template.render(color=color, block=block,type=type)
    verb_print(rendered_content) 
    return rendered_content

def generate_wall_string(color,block):
    with open(f"{WALL_TEMPLATES_PATH}\\walls.j2") as file:
        template_content = file.read()
    template = jinja2.Template(template_content)

    rendered_content = template.render(color=color, block=block)
    verb_print(rendered_content) 
    return rendered_content

def generate_resource_json(color,block,template_path, type=""):
    with open(template_path) as file:
        template_content = file.read()

    template = jinja2.Template(template_content)

    rendered_content = template.render(color=color, block=block, type=type)
    json_data = json.loads(rendered_content)
    pretty_json = json.dumps(json_data, indent=4)
    verb_print(pretty_json)
    return json_data    

def create_json_file(json_data,path):
    if args.dryrun:
        print("dryrun, not creating any files")
    else:
        with open(path, 'w') as file:
            # Write the JSON data to the file
            json.dump(json_data, file, indent=4)

def generate_slab_json_configs(color,block):
    blockstate_json = generate_resource_json(color,block,f"{SLAB_TEMPLATES_PATH}\\slab_blockstate.j2")
    loot_table_json = generate_resource_json(color,block,f"{SLAB_TEMPLATES_PATH}\\slab_loot_tables.j2")
    models_block_json = generate_resource_json(color,block,f"{SLAB_TEMPLATES_PATH}\\slab_models_block.j2")
    models_item_json = generate_resource_json(color,block,f"{SLAB_TEMPLATES_PATH}\\slab_models_item.j2")
    recipe_stonecutter_json = generate_resource_json(color,block,f"{SLAB_TEMPLATES_PATH}\\slab_recipe_stonecutter.j2")
    recipe_json = generate_resource_json(color,block,f"{SLAB_TEMPLATES_PATH}\\slab_recipe.j2")
    top_models_block_json = generate_resource_json(color,block,f"{SLAB_TEMPLATES_PATH}\\slab_top_models_block.j2")

    create_json_file(blockstate_json, f"{BLOCKSTATES_PATH}\\{color}_{block}_slab.json")
    create_json_file(loot_table_json, f"{LOOT_TABLE_PATH}\\{color}_{block}_slab.json")
    create_json_file(models_block_json, f"{MODELS_BLOCK_PATH}\\{color}_{block}_slab.json")
    create_json_file(top_models_block_json, f"{MODELS_BLOCK_PATH}\\{color}_{block}_slab_top.json")
    create_json_file(models_item_json, f"{MODELS_ITEM_PATH}\\{color}_{block}_slab.json")
    create_json_file(recipe_json, f"{RECIPES_PATH}\\{color}_{block}_slab.json")
    create_json_file(recipe_stonecutter_json, f"{RECIPES_PATH}\\{color}_{block}_slab_from_stonecutter.json")

def generate_wall_json_configs(color,block):
    blockstate_json = generate_resource_json(color,block,f"{WALL_TEMPLATES_PATH}\\wall_blockstate.j2")
    models_block_inventory_json = generate_resource_json(color,block,f"{WALL_TEMPLATES_PATH}\\wall_models_block_inventory.j2")
    models_block_post_json = generate_resource_json(color,block,f"{WALL_TEMPLATES_PATH}\\wall_models_block_post.j2")
    models_block_side_tall_json = generate_resource_json(color,block,f"{WALL_TEMPLATES_PATH}\\wall_models_block_side_tall.j2")
    models_block_side_json = generate_resource_json(color,block,f"{WALL_TEMPLATES_PATH}\\wall_models_block_side.j2")
    models_block_tall_json = generate_resource_json(color,block,f"{WALL_TEMPLATES_PATH}\\wall_models_block_tall.j2")
    models_item_json = generate_resource_json(color,block,f"{WALL_TEMPLATES_PATH}\\wall_models_item.j2")
    recipe_stonecutter_json = generate_resource_json(color,block,f"{WALL_TEMPLATES_PATH}\\wall_recipe_stonecutter.j2")
    recipe_json = generate_resource_json(color,block,f"{WALL_TEMPLATES_PATH}\\wall_recipe.j2")

    loot_table_json = generate_resource_json(color,block,f"{GENERAL_TEMPLATES_PATH}\\generic_loot_tables.j2", type="wall")
    wall_string = generate_wall_string(color,block)

    create_json_file(blockstate_json, f"{BLOCKSTATES_PATH}\\{color}_{block}_wall.json")
    create_json_file(models_block_inventory_json, f"{MODELS_BLOCK_PATH}\\{color}_{block}_wall_inventory.json")
    create_json_file(models_block_post_json, f"{MODELS_BLOCK_PATH}\\{color}_{block}_wall_post.json")
    create_json_file(models_block_side_tall_json, f"{MODELS_BLOCK_PATH}\\{color}_{block}_wall_side_tall.json")
    create_json_file(models_block_side_json, f"{MODELS_BLOCK_PATH}\\{color}_{block}_wall_side.json")
    create_json_file(models_block_tall_json, f"{MODELS_BLOCK_PATH}\\{color}_{block}_wall_tall.json")
    create_json_file(models_item_json, f"{MODELS_ITEM_PATH}\\{color}_{block}_wall.json")
    create_json_file(recipe_stonecutter_json, f"{RECIPES_PATH}\\{color}_{block}_wall_from_stonecutter.json")
    create_json_file(recipe_json, f"{RECIPES_PATH}\\{color}_{block}_wall.json")
    create_json_file(loot_table_json, f"{LOOT_TABLE_PATH}\\{color}_{block}_wall.json")
    add_value_to_json(WALL_JSON_PATH,wall_string)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process the type parameter.')
    parser.add_argument('--type', choices=TYPE_CHOICES, help='The type parameter (stairs, wall, or slab)', required=True)
    parser.add_argument('--block', choices=BLOCK_CHOICES, help='The type parameter (concrete, terracotta, or glazed_terracotta)', required=True)
    parser.add_argument('--color', choices=COLOR_CHOICES, help='See minecraft wiki for list of colors', required=True)
    parser.add_argument('--verbose', action="store_true", help = "debug print")
    parser.add_argument('--dryrun', action="store_true", help="no file modification or creation")

    args = parser.parse_args()

    color = args.color
    type = args.type
    block = args.block

    for color in COLOR_CHOICES:
        pickaxe_String = generate_pickaxe_string(color,block,type)
        lang_string = generate_lang_string(color,block,type)

        
        add_kv_pair_to_json(f"{EN_US_LANG_JSON_PATH}",lang_string)
        add_value_to_json(f"{PICKAXE_PATH}",pickaxe_String)

    if args.type == "slab":
        pass
        # for color in COLOR_CHOICES:
        generate_slab_json_configs(color,block)
    if args.type == "wall":
        for color in COLOR_CHOICES:
            generate_wall_json_configs(color,block)
