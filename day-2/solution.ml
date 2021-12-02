open Stdio


type position = {
    depth: int;
    horizontal: int;
    aim: int;
};;

type movement = 
  | Forward of int
  | Down of int
  | Up of int;;

let movement_of_string line = 
  let components = String.split_on_char ' ' line in
  match components with 
    | "forward":: ns :: [] -> Forward (int_of_string ns)
    | "down":: ns :: [] -> Down (int_of_string ns)
    | "up":: ns :: [] -> Up (int_of_string ns)
    | _ -> failwith "Invalid Input"

let movements = List.map movement_of_string (In_channel.input_lines( open_in "./input"));;

let apply_move { depth = prev_depth; horizontal = prev_horizontal; _ } move = match move with 
  | Forward amount -> { depth = prev_depth; horizontal = prev_horizontal + amount; aim = 0 }
  | Down amount -> { depth = prev_depth + amount; horizontal = prev_horizontal; aim = 0 }
  | Up amount -> { depth = prev_depth - amount; horizontal = prev_horizontal; aim = 0 };;

let result = List.fold_left apply_move {depth = 0; horizontal = 0; aim = 0} movements;;

print_int (result.horizontal * result.depth);;
print_string "\n";;

let apply_move2 {depth = prev_depth; horizontal = prev_horizontal; aim = prev_aim} move = match move with
  | Forward amount -> { depth = prev_depth + amount * prev_aim; horizontal = prev_horizontal + amount; aim = prev_aim}
  | Down amount -> { depth = prev_depth; horizontal = prev_horizontal; aim = prev_aim + amount }
  | Up amount -> { depth = prev_depth; horizontal = prev_horizontal; aim = prev_aim - amount }

let result2 = List.fold_left apply_move2 {depth = 0; horizontal = 0; aim = 0} movements;;

print_int (result2.horizontal * result2.depth);;
print_string "\n";;
