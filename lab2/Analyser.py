from src.TruthTableBuilder import TruthTableBuilder
from src.CanonicalFormsBuilder import CanonicalFormsBuilder
from src.ZhegalkinBuilder import ZhegalkinBuilder
from src.PostAnalyser import PostAnalyser
from src.FictiveVariablesFinder import FictiveVariablesFinder
from src.DerivativeAnalyzer import DerivativeAnalyzer
from src.CalculationMinimizer import CalculationMinimizer
from src.CalculationTabularMinimizer import CalculationTabularMinimizer
from src.KarnaughMinimizer import KarnaughMinimizer
from src.Validator import Validator

class Analyser:
    def __init__(
            self,
            validator: Validator | None = None,
            canonical_forms_builder: CanonicalFormsBuilder | None = None,
            zhegalkin_builder: ZhegalkinBuilder | None = None,
            post_analyser: PostAnalyser | None = None,
            derivative_analyzer: DerivativeAnalyzer | None = None, 
            minimizer: CalculationMinimizer | None = None,
            karnaugh_minimizer: KarnaughMinimizer | None = None,
            calculation_tabular_minimizer: CalculationTabularMinimizer | None = None
            ):
        self.validator = validator or Validator()
        self.canonical_forms_builder = canonical_forms_builder or CanonicalFormsBuilder()
        self.zhegalkin_builder = zhegalkin_builder or ZhegalkinBuilder()
        self.post_analyser = post_analyser or PostAnalyser()
        self.derivative_analyzer = derivative_analyzer or DerivativeAnalyzer()
        self.minimizer = minimizer or CalculationMinimizer()
        self.karnaugh_minimizer = karnaugh_minimizer or KarnaughMinimizer()
        self.calculation_tabular_minimizer = calculation_tabular_minimizer or CalculationTabularMinimizer()

    def execute(self, exp):
        self.validator = Validator()
        if not self.validator.validate_expression(exp):
            print(self.validator.get_message())
            return

        table = TruthTableBuilder.build(exp)
        print(table)
        sknf = self.canonical_forms_builder.build_sknf(table)
        sdnf = self.canonical_forms_builder.build_sdnf(table)
        print("СКНФ:", sknf)
        print("СДНФ:", sdnf)

        self.canonical_forms_builder.to_numeric_form(table)
        num_sknf, num_sdnf = self.canonical_forms_builder.get_num_sknf(), self.canonical_forms_builder.get_num_sdnf()
        print("\nСКНФ (числовая форма):", num_sknf)
        print("СДНФ (числовая форма):", num_sdnf)

        index_form = self.canonical_forms_builder.get_index_form(table)
        print("Индексная форма функции:", index_form)

        self.zhegalkin_builder.build(table)

        self.post_analyser.execute(table)
        print("\nСвойства функции:")
        print("T0:", self.post_analyser.t0)
        print("T1:", self.post_analyser.t1)
        print("S:", self.post_analyser.s)
        print("M:", self.post_analyser.m)
        print("L:", self.zhegalkin_builder.is_linear())

        print("\nФиктивные переменные:", FictiveVariablesFinder.find(table))

        self.derivative_analyzer.analyze(table)
        self.derivative_analyzer.print_derivative_canonical_forms()
        print()

        sknf = self.minimizer.minimize_sknf(table)
        sdnf = self.minimizer.minimize_sdnf(table)
        print("Минимизированная СКНФ (расчетный метод): ", sknf)
        print("Минимизированная СДНФ (расчетный метод): ", sdnf)
        
        print()
        sknf = self.calculation_tabular_minimizer.minimize_sknf(table)
        sdnf = self.calculation_tabular_minimizer.minimize_sdnf(table)
        print("Минимизированная СКНФ (расчетно-табличный метод):", sknf)
        print("Минимизированная СДНФ (расчетно-табличный метод):", sdnf)

        self.karnaugh_minimizer.print_karnaugh_map(table)
        print("\nМинимизированная СКНФ (карта Карно):", self.karnaugh_minimizer.minimize_sknf(table))
        print("Минимизированная СДНФ (карта Карно):", self.karnaugh_minimizer.minimize_sdnf(table))



        
