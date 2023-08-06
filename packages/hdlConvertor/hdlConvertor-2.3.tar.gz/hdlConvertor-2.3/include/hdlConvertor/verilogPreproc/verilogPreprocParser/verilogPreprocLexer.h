
// Generated from /home/circleci/project/grammars/verilogPreprocLexer.g4 by ANTLR 4.7.2

#pragma once


#include "antlr4-runtime.h"


namespace verilogPreproc_antlr {


class  verilogPreprocLexer : public antlr4::Lexer {
public:
  enum {
    STR = 1, LINE_COMMENT = 2, COMMENT = 3, CODE = 4, MACRO_ENTER = 5, INCLUDE = 6, 
    DEFINE = 7, IFNDEF = 8, IFDEF = 9, ELSIF = 10, ELSE = 11, ENDIF = 12, 
    UNDEF = 13, BEGIN_KEYWORDS = 14, END_KEYWORDS = 15, PRAGMA = 16, UNDEFINEALL = 17, 
    RESETALL = 18, CELLDEFINE = 19, ENDCELLDEFINE = 20, TIMESCALE = 21, 
    DEFAULT_NETTYPE = 22, LINE = 23, UNCONNECTED_DRIVE = 24, NOUNCONNECTED_DRIVE = 25, 
    PROTECTED = 26, OTHER_MACRO_CALL_WITH_ARGS = 27, OTHER_MACRO_CALL_NO_ARGS = 28, 
    DM_LINE_COMMENT = 29, DM_COMMENT = 30, LINE_ESCAPE = 31, LP = 32, RP = 33, 
    COMMA = 34, EQUAL = 35, DM_NEW_LINE = 36, WS = 37, ID = 38, EXPR_MODE_RP = 39, 
    EXPR_MODE_COMMA = 40, DB_LINE_ESCAPE = 41, NEW_LINE = 42, MA_COMMA = 43, 
    MA_RP = 44, NUM = 45, WIRE = 46, TRI = 47, TRI0 = 48, TRI1 = 49, WAND = 50, 
    TRIAND = 51, WOR = 52, TRIOR = 53, TRIREG = 54, UWIRE = 55, NONE = 56, 
    LINE_MODE_WS = 57, Time_Identifier = 58, TIMING_SPEC_MODE_SLASH = 59, 
    TIMING_SPEC_MODE_WS = 60, INCLUDE_MODE_MACRO_ENTER = 61, INCLUDE_MODE_WS = 62, 
    PRAGMA_WS = 63, PROTECTED_WS = 64, ENDPROTECTED = 65, PROTECTED_LINE = 66, 
    PRAGMA_EQUAL = 67
  };

  enum {
    CH_LINE_ESCAPE = 2, CH_LINE_COMMENT = 3, CH_COMMENT = 4
  };

  enum {
    DIRECTIVE_MODE = 1, DEFINE_MODE = 2, EXPR_MODE = 3, DEFINE_BODY_MODE = 4, 
    MACRO_ARG_LIST_MODE = 5, IFDEF_MODE = 6, UNDEF_MODE = 7, DEFAULT_NETTYPE_MODE = 8, 
    LINE_MODE = 9, TIMING_SPEC_MODE = 10, KEYWOORDS_MODE = 11, INCLUDE_MODE = 12, 
    PRAGMA_MODE = 13, PROTECTED_MODE = 14
  };

  verilogPreprocLexer(antlr4::CharStream *input);
  ~verilogPreprocLexer();



  struct expression_parsing_meta_info {
      int parenthesis;
      int braces;
      int square_braces;
      // parse new expression if there is ',' behind this expression
      bool reenter_expr_on_tailing_comma;

      bool exit_from_parent_mode_on_lp;
      bool next_mode_set;
      // this mode is used if there is ')' which is not part of this expression
      // instead of parrent mode
      size_t next_mode;

      expression_parsing_meta_info() {
          reset();
          exit_from_parent_mode_on_lp = false;
      }
      inline bool no_brace_active() {
          return parenthesis == 0 && braces == 0 && square_braces == 0;
      }
      inline void reset() {
          parenthesis = 0;
          braces = 0;
          square_braces = 0;
          reenter_expr_on_tailing_comma = false;
          exit_from_parent_mode_on_lp = false;
          next_mode_set = false;
          next_mode = 0;
      }
      inline void reset(bool _exit_from_parent_mode_on_lp, bool _reenter_expr_on_tailing_comma) {
          reset();
          reenter_expr_on_tailing_comma = _reenter_expr_on_tailing_comma;
          exit_from_parent_mode_on_lp = _exit_from_parent_mode_on_lp;
          next_mode_set = false;
      }
      inline void reset(bool _exit_from_parent_mode_on_lp, bool _reenter_expr_on_tailing_comma, size_t _next_mode) {
          reset();
          reenter_expr_on_tailing_comma = _reenter_expr_on_tailing_comma;
          exit_from_parent_mode_on_lp = _exit_from_parent_mode_on_lp;
          next_mode = _next_mode;
          next_mode_set = true;
      }
  };

  bool define_in_def_val = false;
  bool define_param_LP_seen = 0;
  bool macro_call_LP_seen = false;
  expression_parsing_meta_info expr_p_meta;

  inline std::string cut_off_line_comment(const std::string & str) {
      auto lc = str.find("//");
      if (lc != std::string::npos) {
          return str.substr(0, lc);
      }
      return str;
  }


  virtual std::string getGrammarFileName() const override;
  virtual const std::vector<std::string>& getRuleNames() const override;

  virtual const std::vector<std::string>& getChannelNames() const override;
  virtual const std::vector<std::string>& getModeNames() const override;
  virtual const std::vector<std::string>& getTokenNames() const override; // deprecated, use vocabulary instead
  virtual antlr4::dfa::Vocabulary& getVocabulary() const override;

  virtual const std::vector<uint16_t> getSerializedATN() const override;
  virtual const antlr4::atn::ATN& getATN() const override;

  virtual void action(antlr4::RuleContext *context, size_t ruleIndex, size_t actionIndex) override;
private:
  static std::vector<antlr4::dfa::DFA> _decisionToDFA;
  static antlr4::atn::PredictionContextCache _sharedContextCache;
  static std::vector<std::string> _ruleNames;
  static std::vector<std::string> _tokenNames;
  static std::vector<std::string> _channelNames;
  static std::vector<std::string> _modeNames;

  static std::vector<std::string> _literalNames;
  static std::vector<std::string> _symbolicNames;
  static antlr4::dfa::Vocabulary _vocabulary;
  static antlr4::atn::ATN _atn;
  static std::vector<uint16_t> _serializedATN;


  // Individual action functions triggered by action() above.
  void CODEAction(antlr4::RuleContext *context, size_t actionIndex);
  void DEFINEAction(antlr4::RuleContext *context, size_t actionIndex);
  void OTHER_MACRO_CALL_WITH_ARGSAction(antlr4::RuleContext *context, size_t actionIndex);
  void DM_LINE_COMMENTAction(antlr4::RuleContext *context, size_t actionIndex);
  void DM_COMMENTAction(antlr4::RuleContext *context, size_t actionIndex);
  void LPAction(antlr4::RuleContext *context, size_t actionIndex);
  void RPAction(antlr4::RuleContext *context, size_t actionIndex);
  void EQUALAction(antlr4::RuleContext *context, size_t actionIndex);
  void DM_NEW_LINEAction(antlr4::RuleContext *context, size_t actionIndex);
  void WSAction(antlr4::RuleContext *context, size_t actionIndex);
  void DN_CODEAction(antlr4::RuleContext *context, size_t actionIndex);
  void EXPR_MODE_LPAction(antlr4::RuleContext *context, size_t actionIndex);
  void EXPR_MODE_RPAction(antlr4::RuleContext *context, size_t actionIndex);
  void EXPR_MODE_LBRAction(antlr4::RuleContext *context, size_t actionIndex);
  void EXPR_MODE_RBRAction(antlr4::RuleContext *context, size_t actionIndex);
  void EXPR_MODE_LSQRAction(antlr4::RuleContext *context, size_t actionIndex);
  void EXPR_MODE_RSQRAction(antlr4::RuleContext *context, size_t actionIndex);
  void EXPR_MODE_COMMAAction(antlr4::RuleContext *context, size_t actionIndex);
  void DB_CODEAction(antlr4::RuleContext *context, size_t actionIndex);
  void MA_COMMAAction(antlr4::RuleContext *context, size_t actionIndex);
  void MA_RPAction(antlr4::RuleContext *context, size_t actionIndex);
  void MA_CODEAction(antlr4::RuleContext *context, size_t actionIndex);

  // Individual semantic predicate functions triggered by sempred() above.

  struct Initializer {
    Initializer();
  };
  static Initializer _init;
};

}  // namespace verilogPreproc_antlr
