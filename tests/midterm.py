from camoulette import Groupe, Exercice, Test, Config


class Midterm(Groupe):

    warning = True  # enable warning (default False)
    timeout = 0.3
    extra_args = []  # ocaml extra args
    prelude = ""  # code to inject between the load and the program

    class Simple(Groupe):

        load = ["list_tools.ml"]  # file to load

        class Length(Exercice):

            prototype = ["val length: list:'a list -> int = <fun>"]
            correction = """
            let length = function
                | [] -> 0
                | e::l -> 1 + lenght l
            ;;
            """

            class Empty(Test):
                coef = 3

                test = """
                print_int (length []);;
                """

                stdout = "0"

            class One(Test):

                test = """
                print_int (length [1]);;
                """

                stdout = "2"

            class Some(Test):

                test = """
                print_int (length [1;2;4]);;
                """

                stdout = "3"

            class ALot(Test):

                def test(self):
                    return "print_int (length [" + \
                        ";".join(map(str, list(range(1000)))) + "]);;"

                stdout = "1000"

        class Nth(Exercice):

            prototype = ["val nth: i:int -> queue:'a list -> 'a = <func>"]
            correction = """
            let nth i l =
                if i < 0 then
                    invalid_arg "nth: invalid arg"
                else
                    let rec aux = function
                        | (_, []) -> failure "nth: some error"
                        | (0, e:: l) -> e
                        | (i, e:: l) -> aux (i - 1, l)
                    in
                    aux(i, l)
            ; ;
            """

            class NegativeIndex(Test):

                coef = 0.5

                test = """
                print_list print_int (nth (-1) [1; 2; 4]); ;
                """

                error_code = 2
                stderr = 'Exception: Invalid_argument "nth: ...".'

            class Overflow(Test):

                coef = 0.5

                test = """
                print_list print_int (nth 3 [1; 2; 4]); ;
                """

                error_code = 2
                # si non presiser dans le sujet vous pouvez metre que le le type
                # ou meme que une Exception
                stderr = 'Exception: '
                stderr = 'Exception: Failure '


if __name__ == '__main__':
    config: Config = Config.from_args()
    Midterm().run(config)
