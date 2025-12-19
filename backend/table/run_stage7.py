from table.table_detector import detect_nutrition_blocks
from table.nutrition_table_parser import parse_nutrition_table

def run_stage7(text_blocks):
    nutrition_blocks = detect_nutrition_blocks(text_blocks)
    parsed_nutrition = parse_nutrition_table(nutrition_blocks)
    return parsed_nutrition
