

#include <hdlConvertor/language.h>



// Generated from /home/circleci/project/grammars/verilogPreprocParser.g4 by ANTLR 4.7.2

#pragma once


#include "antlr4-runtime.h"
#include "verilogPreprocParserVisitor.h"


namespace verilogPreproc_antlr {

/**
 * This class provides an empty implementation of verilogPreprocParserVisitor, which can be
 * extended to create a visitor which only needs to handle a subset of the available methods.
 */
class  verilogPreprocParserBaseVisitor : public verilogPreprocParserVisitor {
public:

  virtual antlrcpp::Any visitFile(verilogPreprocParser::FileContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitText(verilogPreprocParser::TextContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitPreprocess_directive(verilogPreprocParser::Preprocess_directiveContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitDefine(verilogPreprocParser::DefineContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitDefine_args(verilogPreprocParser::Define_argsContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitDefine_args_with_def_val(verilogPreprocParser::Define_args_with_def_valContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitParam_with_def_val(verilogPreprocParser::Param_with_def_valContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitDefine_args_basic(verilogPreprocParser::Define_args_basicContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitReplacement(verilogPreprocParser::ReplacementContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitDefault_text(verilogPreprocParser::Default_textContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitConditional(verilogPreprocParser::ConditionalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitIfdef_directive(verilogPreprocParser::Ifdef_directiveContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitIfndef_directive(verilogPreprocParser::Ifndef_directiveContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitElse_group_of_lines(verilogPreprocParser::Else_group_of_linesContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitGroup_of_lines(verilogPreprocParser::Group_of_linesContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitMacro_call(verilogPreprocParser::Macro_callContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitValue(verilogPreprocParser::ValueContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitMacro_id(verilogPreprocParser::Macro_idContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitVar_id(verilogPreprocParser::Var_idContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitCond_id(verilogPreprocParser::Cond_idContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUndef(verilogPreprocParser::UndefContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitCelldefine(verilogPreprocParser::CelldefineContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitEndcelldefine(verilogPreprocParser::EndcelldefineContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUnconnected_drive(verilogPreprocParser::Unconnected_driveContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitNounconnected_drive(verilogPreprocParser::Nounconnected_driveContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitDefault_nettype(verilogPreprocParser::Default_nettypeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitDefault_nettype_value(verilogPreprocParser::Default_nettype_valueContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitLine_directive(verilogPreprocParser::Line_directiveContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitTiming_spec(verilogPreprocParser::Timing_specContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitProtected_block(verilogPreprocParser::Protected_blockContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitResetall(verilogPreprocParser::ResetallContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitUndefineall(verilogPreprocParser::UndefineallContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitKeywords_directive(verilogPreprocParser::Keywords_directiveContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitVersion_specifier(verilogPreprocParser::Version_specifierContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitEndkeywords_directive(verilogPreprocParser::Endkeywords_directiveContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitInclude(verilogPreprocParser::IncludeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitPragma(verilogPreprocParser::PragmaContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitPragma_name(verilogPreprocParser::Pragma_nameContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitPragma_expression(verilogPreprocParser::Pragma_expressionContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitPragma_value(verilogPreprocParser::Pragma_valueContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual antlrcpp::Any visitPragma_keyword(verilogPreprocParser::Pragma_keywordContext *ctx) override {
    return visitChildren(ctx);
  }


};

}  // namespace verilogPreproc_antlr
