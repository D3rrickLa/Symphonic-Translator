import mido 
from src.profile_detection import ProfileDetection
from MidiItem import Actions
import subprocess
from keyboard import send

def list_midi_devices():
    print("Available MIDI Input Ports:")
    for port in mido.get_input_names():
        print(port)

def execute_action(action_conf):
    if not action_conf or "action" not in action_conf:
       print("No action configured")
       return
    
    action_type = action_conf["action"]
    parameters = action_conf.get("params", {})


    try:
        match int(action_type):
            case Actions.RUN_COMMAND.value:
                command = parameters.get("RUN_COMMAND", "")
                subprocess.run(command, shell=True) if command else print("No command provided for 'run_command'.")    

            case Actions.KEYBOARD_SHORTCUT.value:
                keys = parameters.get("KEYBOARD_SHORTCUT", "")
                send(keys) if keys else  print("No keys provided for 'keyboard_shortcut'.")
             
            case Actions.RUN_SCRIPT.value:
                script = parameters.get("RUN_SCRIPT", "")
                subprocess.run(["python", script], shell=True) if script else print("No script provided for 'run_script'.")
                    
            case "print_message": # TODO get rid of this
                message = parameters.get("PRINT_MESSAGE", "No message provided.")
                print(message)
            case Actions.NONE.value: # TODO get rid of this
                print("No action assigned to this input")
            case _:
                print(f"Unknown action type: {action_type}")

    except Exception as e:
        print(f"Error executing action: {e}")

def listen_to_midi(midi_device):
    try:
        with mido.open_input(midi_device) as port:
            for msg in port:
                active_profile = ProfileDetection().run_app()
                match msg.type:
                    case "note_on" if msg.velocity > 0:
                        action = active_profile["KEY"].get(str(msg.note))
                        print(action)
                        execute_action(action)
                       
                        if(msg.note == 72):
                            break

                    case "control_change":
                        action = active_profile["cc"].get(str(msg.control))
                        execute_action(action)

                    case "pitchwheel":
                        action = active_profile["pw"].get('1')
                        execute_action(action)
                    
                

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_midi_devices()
    # selected_device = input("please enter the selected MIDI device:")
    listen_to_midi("Minilab3 MIDI 0")


#  pyinstaller.exe --onefile .\testing\mapping.py