instructions = [
 {
  "instruction": "mov",
  "destination_register": "edi",
  "data": 0x23
}, {
  "instruction": "mov",
  "source_register": "edi",
  "destination_register": "eax",
  "source_type": "register",
  "destination_type": "register"
},
{
  "instruction": "ret"
}]

instruction_lookup = {
  "mov": {"immediate": 0x8b, "register": 0x8B, "by_register": {
    "edi": 0xbf
  }},
  "ret": {"register": 0xc3, "immediate": 0xc3}
}

registers = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]
# EAX
# 000	ECX
# 001	EDX
# 010	EBX
# 011	ESP
# 100	EBP
# 101	ESI
# 110	EDI


def assemble(instructions):
  
  outputs = []
  
  for instruction in instructions:
    print("#####")
    data = []
    second_byte = 0x0000
    instruction_data = instruction_lookup[instruction["instruction"]]
    if "data" in instruction:
      if "by_register" in instruction_data:
        opcode = instruction_data["by_register"][instruction["destination_register"]]
      else:
        opcode = instruction_data["immediate"]
      second_byte = instruction["data"]
    
    else:
      opcode = instruction_data["register"]
    data.append(opcode)
    data.append(second_byte)
    print(data)
    reg = 0
    mod = 0
    rm = 0
    
    print(instruction_data)
    print(instruction)

    if "data" not in instruction:
      if "source_type" in instruction and instruction["source_type"] == "register":
        print("source type is a register")
        mod = 3
        print("mode is {}".format(mod))
        if "source_register" in instruction and instruction["source_register"] in registers:
          rm = registers.index(instruction["source_register"])
          print("rm is {}".format(rm))
      if "destination_register" in instruction and instruction["destination_register"] in registers:
        
        reg = registers.index(instruction["destination_register"])
        print("destination register is {}".format(reg))

    components = [opcode, second_byte, mod, reg, rm]
    byte_1 = "{:8b}".format(opcode)
    byte_2 = "{:8b}".format(second_byte)
    
    
    byte_3 = "{:8b}".format(0x00)
    byte_7 = "{:8b}".format(0x00)
    
    byte_5 = "{:8b}".format(0x00)
    byte_6 = "{:8b}".format(0x00)

    byte_8 = "{:8b}".format(0x00)

    byte_4 = "{:8b}".format(0x00)
    
    byte_9 = "{:8b}".format(0x00)
    binary = '{:8b}{:03b}{:02b}{:03b}{:b}'.format(*components)
    output = []
    if "data" in instruction:
      bytes = [byte_1, byte_2, byte_3, byte_4, byte_5]
    else:
      byte_2 = "{:02b}{:03b}{:03b}".format(mod, reg, rm)
      bytes = [byte_1, byte_2]

    # if "data" in instruction:
    #   bytes.append("{:8b}".format(second_byte))
    #   bytes.append("{:8b}".format(0x00))
    #   bytes.append("{:8b}".format(0x00))
    #   bytes.append("{:8b}".format(0x00))
      
    for byte in bytes:
      hexdata = hex(int(byte, 2))
      if hexdata == "0x0":
        output.append("0x00")
      else:
        output.append(hexdata)

    print(hex(int(binary, 2)))
    print(output)
    
    outputs.append(output)
  print("0x")
  for output in outputs:
    for suboutput in output:
      
      print(suboutput.replace("0x", ""), end="")
    
  print("")

assemble(instructions)
