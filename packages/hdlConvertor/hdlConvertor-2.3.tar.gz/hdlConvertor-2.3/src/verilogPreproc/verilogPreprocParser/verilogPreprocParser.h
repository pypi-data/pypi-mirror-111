

#include <hdlConvertor/language.h>



// Generated from /home/circleci/project/grammars/verilogPreprocParser.g4 by ANTLR 4.7.2

#pragma once


#include "antlr4-runtime.h"


namespace verilogPreproc_antlr {


class  verilogPreprocParser : public antlr4::Parser {
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
    RuleFile = 0, RuleText = 1, RulePreprocess_directive = 2, RuleDefine = 3, 
    RuleDefine_args = 4, RuleDefine_args_with_def_val = 5, RuleParam_with_def_val = 6, 
    RuleDefine_args_basic = 7, RuleReplacement = 8, RuleDefault_text = 9, 
    RuleConditional = 10, RuleIfdef_directive = 11, RuleIfndef_directive = 12, 
    RuleElse_group_of_lines = 13, RuleGroup_of_lines = 14, RuleMacro_call = 15, 
    RuleValue = 16, RuleMacro_id = 17, RuleVar_id = 18, RuleCond_id = 19, 
    RuleUndef = 20, RuleCelldefine = 21, RuleEndcelldefine = 22, RuleUnconnected_drive = 23, 
    RuleNounconnected_drive = 24, RuleDefault_nettype = 25, RuleDefault_nettype_value = 26, 
    RuleLine_directive = 27, RuleTiming_spec = 28, RuleProtected_block = 29, 
    RuleResetall = 30, RuleUndefineall = 31, RuleKeywords_directive = 32, 
    RuleVersion_specifier = 33, RuleEndkeywords_directive = 34, RuleInclude = 35, 
    RulePragma = 36, RulePragma_name = 37, RulePragma_expression = 38, RulePragma_value = 39, 
    RulePragma_keyword = 40
  };

  verilogPreprocParser(antlr4::TokenStream *input);
  ~verilogPreprocParser();

  virtual std::string getGrammarFileName() const override;
  virtual const antlr4::atn::ATN& getATN() const override { return _atn; };
  virtual const std::vector<std::string>& getTokenNames() const override { return _tokenNames; }; // deprecated: use vocabulary instead.
  virtual const std::vector<std::string>& getRuleNames() const override;
  virtual antlr4::dfa::Vocabulary& getVocabulary() const override;



  hdlConvertor::Language language_version;



  class FileContext;
  class TextContext;
  class Preprocess_directiveContext;
  class DefineContext;
  class Define_argsContext;
  class Define_args_with_def_valContext;
  class Param_with_def_valContext;
  class Define_args_basicContext;
  class ReplacementContext;
  class Default_textContext;
  class ConditionalContext;
  class Ifdef_directiveContext;
  class Ifndef_directiveContext;
  class Else_group_of_linesContext;
  class Group_of_linesContext;
  class Macro_callContext;
  class ValueContext;
  class Macro_idContext;
  class Var_idContext;
  class Cond_idContext;
  class UndefContext;
  class CelldefineContext;
  class EndcelldefineContext;
  class Unconnected_driveContext;
  class Nounconnected_driveContext;
  class Default_nettypeContext;
  class Default_nettype_valueContext;
  class Line_directiveContext;
  class Timing_specContext;
  class Protected_blockContext;
  class ResetallContext;
  class UndefineallContext;
  class Keywords_directiveContext;
  class Version_specifierContext;
  class Endkeywords_directiveContext;
  class IncludeContext;
  class PragmaContext;
  class Pragma_nameContext;
  class Pragma_expressionContext;
  class Pragma_valueContext;
  class Pragma_keywordContext; 

  class  FileContext : public antlr4::ParserRuleContext {
  public:
    FileContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EOF();
    std::vector<TextContext *> text();
    TextContext* text(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  FileContext* file();

  class  TextContext : public antlr4::ParserRuleContext {
  public:
    TextContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Preprocess_directiveContext *preprocess_directive();
    antlr4::tree::TerminalNode *LINE_COMMENT();
    antlr4::tree::TerminalNode *CODE();
    antlr4::tree::TerminalNode *NEW_LINE();
    antlr4::tree::TerminalNode *NUM();
    antlr4::tree::TerminalNode *ID();
    antlr4::tree::TerminalNode *STR();
    antlr4::tree::TerminalNode *COMMENT();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  TextContext* text();

  class  Preprocess_directiveContext : public antlr4::ParserRuleContext {
  public:
    Preprocess_directiveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    DefineContext *define();
    ConditionalContext *conditional();
    Macro_callContext *macro_call();
    ResetallContext *resetall();
    UndefContext *undef();
    IncludeContext *include();
    CelldefineContext *celldefine();
    EndcelldefineContext *endcelldefine();
    Unconnected_driveContext *unconnected_drive();
    Nounconnected_driveContext *nounconnected_drive();
    Default_nettypeContext *default_nettype();
    Line_directiveContext *line_directive();
    Timing_specContext *timing_spec();
    Protected_blockContext *protected_block();
    UndefineallContext *undefineall();
    Keywords_directiveContext *keywords_directive();
    Endkeywords_directiveContext *endkeywords_directive();
    PragmaContext *pragma();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Preprocess_directiveContext* preprocess_directive();

  class  DefineContext : public antlr4::ParserRuleContext {
  public:
    DefineContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DEFINE();
    Macro_idContext *macro_id();
    antlr4::tree::TerminalNode *LINE_COMMENT();
    antlr4::tree::TerminalNode *NEW_LINE();
    antlr4::tree::TerminalNode *EOF();
    antlr4::tree::TerminalNode *LP();
    antlr4::tree::TerminalNode *RP();
    std::vector<antlr4::tree::TerminalNode *> WS();
    antlr4::tree::TerminalNode* WS(size_t i);
    ReplacementContext *replacement();
    Define_argsContext *define_args();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  DefineContext* define();

  class  Define_argsContext : public antlr4::ParserRuleContext {
  public:
    Define_argsContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Define_args_with_def_valContext *define_args_with_def_val();
    Define_args_basicContext *define_args_basic();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Define_argsContext* define_args();

  class  Define_args_with_def_valContext : public antlr4::ParserRuleContext {
  public:
    Define_args_with_def_valContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Param_with_def_valContext *> param_with_def_val();
    Param_with_def_valContext* param_with_def_val(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Define_args_with_def_valContext* define_args_with_def_val();

  class  Param_with_def_valContext : public antlr4::ParserRuleContext {
  public:
    Param_with_def_valContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Var_idContext *var_id();
    antlr4::tree::TerminalNode *EQUAL();
    Default_textContext *default_text();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Param_with_def_valContext* param_with_def_val();

  class  Define_args_basicContext : public antlr4::ParserRuleContext {
  public:
    Define_args_basicContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<Var_idContext *> var_id();
    Var_idContext* var_id(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Define_args_basicContext* define_args_basic();

  class  ReplacementContext : public antlr4::ParserRuleContext {
  public:
    ReplacementContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> CODE();
    antlr4::tree::TerminalNode* CODE(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ReplacementContext* replacement();

  class  Default_textContext : public antlr4::ParserRuleContext {
  public:
    Default_textContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<antlr4::tree::TerminalNode *> CODE();
    antlr4::tree::TerminalNode* CODE(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Default_textContext* default_text();

  class  ConditionalContext : public antlr4::ParserRuleContext {
  public:
    ConditionalContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Ifdef_directiveContext *ifdef_directive();
    Ifndef_directiveContext *ifndef_directive();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ConditionalContext* conditional();

  class  Ifdef_directiveContext : public antlr4::ParserRuleContext {
  public:
    Ifdef_directiveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IFDEF();
    std::vector<Cond_idContext *> cond_id();
    Cond_idContext* cond_id(size_t i);
    std::vector<Group_of_linesContext *> group_of_lines();
    Group_of_linesContext* group_of_lines(size_t i);
    antlr4::tree::TerminalNode *ENDIF();
    std::vector<antlr4::tree::TerminalNode *> ELSIF();
    antlr4::tree::TerminalNode* ELSIF(size_t i);
    antlr4::tree::TerminalNode *ELSE();
    Else_group_of_linesContext *else_group_of_lines();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Ifdef_directiveContext* ifdef_directive();

  class  Ifndef_directiveContext : public antlr4::ParserRuleContext {
  public:
    Ifndef_directiveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *IFNDEF();
    std::vector<Cond_idContext *> cond_id();
    Cond_idContext* cond_id(size_t i);
    std::vector<Group_of_linesContext *> group_of_lines();
    Group_of_linesContext* group_of_lines(size_t i);
    antlr4::tree::TerminalNode *ENDIF();
    std::vector<antlr4::tree::TerminalNode *> ELSIF();
    antlr4::tree::TerminalNode* ELSIF(size_t i);
    antlr4::tree::TerminalNode *ELSE();
    Else_group_of_linesContext *else_group_of_lines();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Ifndef_directiveContext* ifndef_directive();

  class  Else_group_of_linesContext : public antlr4::ParserRuleContext {
  public:
    Else_group_of_linesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Group_of_linesContext *group_of_lines();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Else_group_of_linesContext* else_group_of_lines();

  class  Group_of_linesContext : public antlr4::ParserRuleContext {
  public:
    Group_of_linesContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<TextContext *> text();
    TextContext* text(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Group_of_linesContext* group_of_lines();

  class  Macro_callContext : public antlr4::ParserRuleContext {
  public:
    Macro_callContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *OTHER_MACRO_CALL_NO_ARGS();
    antlr4::tree::TerminalNode *OTHER_MACRO_CALL_WITH_ARGS();
    antlr4::tree::TerminalNode *RP();
    std::vector<ValueContext *> value();
    ValueContext* value(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Macro_callContext* macro_call();

  class  ValueContext : public antlr4::ParserRuleContext {
  public:
    ValueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<TextContext *> text();
    TextContext* text(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ValueContext* value();

  class  Macro_idContext : public antlr4::ParserRuleContext {
  public:
    Macro_idContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ID();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Macro_idContext* macro_id();

  class  Var_idContext : public antlr4::ParserRuleContext {
  public:
    Var_idContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ID();
    std::vector<antlr4::tree::TerminalNode *> COMMENT();
    antlr4::tree::TerminalNode* COMMENT(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Var_idContext* var_id();

  class  Cond_idContext : public antlr4::ParserRuleContext {
  public:
    Cond_idContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ID();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Cond_idContext* cond_id();

  class  UndefContext : public antlr4::ParserRuleContext {
  public:
    UndefContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *UNDEF();
    antlr4::tree::TerminalNode *ID();
    antlr4::tree::TerminalNode *WS();
    antlr4::tree::TerminalNode *NEW_LINE();
    antlr4::tree::TerminalNode *EOF();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  UndefContext* undef();

  class  CelldefineContext : public antlr4::ParserRuleContext {
  public:
    CelldefineContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *CELLDEFINE();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  CelldefineContext* celldefine();

  class  EndcelldefineContext : public antlr4::ParserRuleContext {
  public:
    EndcelldefineContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ENDCELLDEFINE();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  EndcelldefineContext* endcelldefine();

  class  Unconnected_driveContext : public antlr4::ParserRuleContext {
  public:
    Unconnected_driveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *UNCONNECTED_DRIVE();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Unconnected_driveContext* unconnected_drive();

  class  Nounconnected_driveContext : public antlr4::ParserRuleContext {
  public:
    Nounconnected_driveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *NOUNCONNECTED_DRIVE();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Nounconnected_driveContext* nounconnected_drive();

  class  Default_nettypeContext : public antlr4::ParserRuleContext {
  public:
    Default_nettypeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *DEFAULT_NETTYPE();
    Default_nettype_valueContext *default_nettype_value();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Default_nettypeContext* default_nettype();

  class  Default_nettype_valueContext : public antlr4::ParserRuleContext {
  public:
    Default_nettype_valueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *WIRE();
    antlr4::tree::TerminalNode *TRI();
    antlr4::tree::TerminalNode *TRI0();
    antlr4::tree::TerminalNode *TRI1();
    antlr4::tree::TerminalNode *WAND();
    antlr4::tree::TerminalNode *TRIAND();
    antlr4::tree::TerminalNode *WOR();
    antlr4::tree::TerminalNode *TRIOR();
    antlr4::tree::TerminalNode *TRIREG();
    antlr4::tree::TerminalNode *UWIRE();
    antlr4::tree::TerminalNode *NONE();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Default_nettype_valueContext* default_nettype_value();

  class  Line_directiveContext : public antlr4::ParserRuleContext {
  public:
    Line_directiveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LINE();
    std::vector<antlr4::tree::TerminalNode *> NUM();
    antlr4::tree::TerminalNode* NUM(size_t i);
    antlr4::tree::TerminalNode *STR();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Line_directiveContext* line_directive();

  class  Timing_specContext : public antlr4::ParserRuleContext {
  public:
    Timing_specContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *TIMESCALE();
    std::vector<antlr4::tree::TerminalNode *> Time_Identifier();
    antlr4::tree::TerminalNode* Time_Identifier(size_t i);
    antlr4::tree::TerminalNode *TIMING_SPEC_MODE_SLASH();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Timing_specContext* timing_spec();

  class  Protected_blockContext : public antlr4::ParserRuleContext {
  public:
    Protected_blockContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *PROTECTED();
    antlr4::tree::TerminalNode *ENDPROTECTED();
    std::vector<antlr4::tree::TerminalNode *> PROTECTED_LINE();
    antlr4::tree::TerminalNode* PROTECTED_LINE(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Protected_blockContext* protected_block();

  class  ResetallContext : public antlr4::ParserRuleContext {
  public:
    ResetallContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *RESETALL();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ResetallContext* resetall();

  class  UndefineallContext : public antlr4::ParserRuleContext {
  public:
    UndefineallContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *UNDEFINEALL();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  UndefineallContext* undefineall();

  class  Keywords_directiveContext : public antlr4::ParserRuleContext {
  public:
    Keywords_directiveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *BEGIN_KEYWORDS();
    Version_specifierContext *version_specifier();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Keywords_directiveContext* keywords_directive();

  class  Version_specifierContext : public antlr4::ParserRuleContext {
  public:
    Version_specifierContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *STR();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Version_specifierContext* version_specifier();

  class  Endkeywords_directiveContext : public antlr4::ParserRuleContext {
  public:
    Endkeywords_directiveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *END_KEYWORDS();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Endkeywords_directiveContext* endkeywords_directive();

  class  IncludeContext : public antlr4::ParserRuleContext {
  public:
    IncludeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *INCLUDE();
    antlr4::tree::TerminalNode *STR();
    Macro_callContext *macro_call();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  IncludeContext* include();

  class  PragmaContext : public antlr4::ParserRuleContext {
  public:
    PragmaContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *PRAGMA();
    Pragma_nameContext *pragma_name();
    antlr4::tree::TerminalNode *NEW_LINE();
    antlr4::tree::TerminalNode *EOF();
    std::vector<Pragma_expressionContext *> pragma_expression();
    Pragma_expressionContext* pragma_expression(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PragmaContext* pragma();

  class  Pragma_nameContext : public antlr4::ParserRuleContext {
  public:
    Pragma_nameContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ID();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Pragma_nameContext* pragma_name();

  class  Pragma_expressionContext : public antlr4::ParserRuleContext {
  public:
    Pragma_expressionContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    Pragma_keywordContext *pragma_keyword();
    antlr4::tree::TerminalNode *EQUAL();
    Pragma_valueContext *pragma_value();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Pragma_expressionContext* pragma_expression();

  class  Pragma_valueContext : public antlr4::ParserRuleContext {
  public:
    Pragma_valueContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *LP();
    std::vector<Pragma_expressionContext *> pragma_expression();
    Pragma_expressionContext* pragma_expression(size_t i);
    antlr4::tree::TerminalNode *RP();
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);
    antlr4::tree::TerminalNode *NUM();
    antlr4::tree::TerminalNode *STR();
    antlr4::tree::TerminalNode *ID();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Pragma_valueContext* pragma_value();

  class  Pragma_keywordContext : public antlr4::ParserRuleContext {
  public:
    Pragma_keywordContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *ID();

    virtual antlrcpp::Any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  Pragma_keywordContext* pragma_keyword();


  virtual bool sempred(antlr4::RuleContext *_localctx, size_t ruleIndex, size_t predicateIndex) override;
  bool preprocess_directiveSempred(Preprocess_directiveContext *_localctx, size_t predicateIndex);
  bool define_argsSempred(Define_argsContext *_localctx, size_t predicateIndex);
  bool default_nettype_valueSempred(Default_nettype_valueContext *_localctx, size_t predicateIndex);
  bool includeSempred(IncludeContext *_localctx, size_t predicateIndex);

private:
  static std::vector<antlr4::dfa::DFA> _decisionToDFA;
  static antlr4::atn::PredictionContextCache _sharedContextCache;
  static std::vector<std::string> _ruleNames;
  static std::vector<std::string> _tokenNames;

  static std::vector<std::string> _literalNames;
  static std::vector<std::string> _symbolicNames;
  static antlr4::dfa::Vocabulary _vocabulary;
  static antlr4::atn::ATN _atn;
  static std::vector<uint16_t> _serializedATN;


  struct Initializer {
    Initializer();
  };
  static Initializer _init;
};

}  // namespace verilogPreproc_antlr
