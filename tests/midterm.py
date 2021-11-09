from camoulette import CROP, Group, Test
from camoulette.test.test_result import TestResult
from camoulette.utils import FLEXIBLE, STRICT


class Midterm(Group):

    warning = True  # enable warning (default False)
    timeout = 0.3
    extra_args = []  # ocaml extra args
    # code to inject between the load and the program
    prelude = '#use "tests/test_utilities.ml";;'

    class Simple(Group):

        file = 'list_tools.ml'

        class Length(Group):

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

            class TimeOut(Test):

                test = """
                let rec print x = (
                    print_int x;
                    print (x + 1);
                );;
                print 0;;
                """

                stdout = "3"

            class ALot(Test):

                @property
                def test(self):
                    return "print_int (length [" + \
                        ";".join(map(str, range(1000))) + "]);;"

                stdout = "1000"

        class Nth(Group):

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
            ;;
            """

            class Error(Group):

                class NegativeIndex(Test):

                    coef = 0.5

                    test = """
                    print_int (nth (-1) [1; 2; 4]);;
                    """

                    mode = FLEXIBLE

                    returncode = 2
                    stderr = 'Exception: Invalid_argument "nth:'

                class Overflow(Test):

                    coef = 0.5

                    test = """
                    print_int (nth 3 [1; 2; 4]);;
                    """

                    returncode = 2
                    # si non presiser dans le sujet vous pouvez metre que le le type
                    # ou meme que une Exception
                    stderr = 'Exception: '
                    stderr = 'Exception: Failure '

            class Sucess(Group):

                class Simple(Test):

                    test = """
                    print_int (nth 0 [1; 2; 4]);;
                    """
                    stdout = '1'

                class Simple2(Test):

                    test = """
                    print_int (nth 1 [1; 2; 4]);;
                    """
                    stdout = '2'


import sys

if len(sys.argv) != 2:
    print("usage: python3 midterm.py path/to/studient/repo")
    exit(1)

Midterm()(sys.argv[1]).print()
