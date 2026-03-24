from TruthTableBuilder import TruthTableBuilder
from CanonicalFormsBuilder import CanonicalFormsBuilder
from ZhegalkinBuilder import ZhegalkinBuilder
from PostAnalyser import PostAnalyser
from FictiveVariablesFinder import FictiveVariablesFinder
from Derivatives import BooleanDerivativeAnalyzer
from D import DerivativeAnalyzer
from CalculationMinimizer import CalculationMinimizer
from Minimization import Mini
from CalculationTabularMinimizer import CalculationTabularMinimizer
from KarnaughMinimizer import KarnaughMinimizer

class Analyser:
    def __init__(self):
        self.truth_table_builder: TruthTableBuilder = TruthTableBuilder()
        self.canonical_forms_builder: CanonicalFormsBuilder = CanonicalFormsBuilder()
        self.zhegalkin_builder: ZhegalkinBuilder = ZhegalkinBuilder()
        self.post_analyser: PostAnalyser = PostAnalyser()
        self.fictive_variables_finder: FictiveVariablesFinder = FictiveVariablesFinder()
        self.boolean_derivative_analyzer: BooleanDerivativeAnalyzer = BooleanDerivativeAnalyzer()
        self.derivative_analyzer: DerivativeAnalyzer = DerivativeAnalyzer()
        self.minimizer: CalculationMinimizer = CalculationMinimizer()
        self.minimization: Mini = Mini()
        self.karnaugh_minimizer: KarnaughMinimizer = KarnaughMinimizer()

    def execute(self, exp):
        table = self.truth_table_builder.build(exp)
        self.truth_table_builder.print_table(exp, table)
        self.canonical_forms_builder.get_canonical_forms(table, self.truth_table_builder.variables)
        sknf, sdnf = self.canonical_forms_builder.sknf, self.canonical_forms_builder.sdnf
        print("\nСКНФ:", sknf)
        print("СДНФ:", sdnf)
        index_form = self.canonical_forms_builder.get_index_form(table)
        print("Индексная форма функции:", index_form)   
        self.canonical_forms_builder.to_numeric_form(table)
        num_sknf, num_sdnf = self.canonical_forms_builder.num_sknf, self.canonical_forms_builder.num_sdnf
        print("\nСКНФ (числовая форма):", num_sknf)
        print("СДНФ (числовая форма):", num_sdnf)

        index_form = self.canonical_forms_builder.get_index_form(table)
        print("Индексная форма функции:", index_form)

        self.zhegalkin_builder.build(table, self.truth_table_builder.variables)

        self.post_analyser.execute(table)
        print("\nСвойства функции:")
        print("T0:", self.post_analyser.t0)
        print("T1:", self.post_analyser.t1)
        print("S:", self.post_analyser.s)
        print("M:", self.post_analyser.m)
        print("L:", self.zhegalkin_builder.is_linear())

        print("Фиктивные переменные:", self.fictive_variables_finder.find(table, self.truth_table_builder.variables))

        # self.boolean_derivative_analyzer.find(table, self.truth_table_builder.variables)
        # self.boolean_derivative_analyzer.print_derivatives()
        # self.boolean_derivative_analyzer.find_higher_order(table, self.truth_table_builder.variables, 4)
        # self.boolean_derivative_analyzer.print_higher_order_derivatives()

        self.derivative_analyzer.analyze(table, self.truth_table_builder.variables)
        self.derivative_analyzer.print_derivative_canonical_forms()

        self.minimizer.minimize_sknf(table, self.truth_table_builder.variables)
        self.minimizer.minimize_sdnf(table, self.truth_table_builder.variables)
        print("\nМинимизированная СДНФ:", self.minimizer.get_minimized_sdnf())
        print("Минимизированная СКНФ:", self.minimizer.get_minimized_sknf())

        self.minimization.minimize(table, self.truth_table_builder.variables)
        print("\nМинимизированная СДНФ:", self.minimization.get_minimized_sdnf())
        print("Минимизированная СКНФ:", self.minimization.get_minimized_sknf())

        ctm = CalculationTabularMinimizer()
        ctm.minimize_sdnf(table, self.truth_table_builder.variables)
        print("\nМинимизированная СДНФ (расчетно-табличный метод):", ctm.get_minimized_sdnf())
        ctm.minimize_sknf(table, self.truth_table_builder.variables)
        print("Минимизированная СКНФ (расчетно-табличный метод):", ctm.get_minimized_sknf())

        self.karnaugh_minimizer.print_karnaugh_map(table, self.truth_table_builder.variables)
        self.karnaugh_minimizer.minimize_sdnf(table, self.truth_table_builder.variables)
        self.karnaugh_minimizer.minimize_sknf(table, self.truth_table_builder.variables)
        print("\nМинимизированная СДНФ (карта Карно):", self.karnaugh_minimizer.get_minimized_sdnf())
        print("Минимизированная СКНФ (карта Карно):", self.karnaugh_minimizer.get_minimized_sknf())



        
