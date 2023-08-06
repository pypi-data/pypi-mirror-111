

#include <hdlConvertor/language.h>



// Generated from /home/circleci/project/grammars/verilogPreprocParser.g4 by ANTLR 4.7.2

#pragma once


#include "antlr4-runtime.h"
#include "verilogPreprocParser.h"


namespace verilogPreproc_antlr {

/**
 * This class defines an abstract visitor for a parse tree
 * produced by verilogPreprocParser.
 */
class  verilogPreprocParserVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by verilogPreprocParser.
   */
    virtual antlrcpp::Any visitFile(verilogPreprocParser::FileContext *context) = 0;

    virtual antlrcpp::Any visitText(verilogPreprocParser::TextContext *context) = 0;

    virtual antlrcpp::Any visitPreprocess_directive(verilogPreprocParser::Preprocess_directiveContext *context) = 0;

    virtual antlrcpp::Any visitDefine(verilogPreprocParser::DefineContext *context) = 0;

    virtual antlrcpp::Any visitDefine_args(verilogPreprocParser::Define_argsContext *context) = 0;

    virtual antlrcpp::Any visitDefine_args_with_def_val(verilogPreprocParser::Define_args_with_def_valContext *context) = 0;

    virtual antlrcpp::Any visitParam_with_def_val(verilogPreprocParser::Param_with_def_valContext *context) = 0;

    virtual antlrcpp::Any visitDefine_args_basic(verilogPreprocParser::Define_args_basicContext *context) = 0;

    virtual antlrcpp::Any visitReplacement(verilogPreprocParser::ReplacementContext *context) = 0;

    virtual antlrcpp::Any visitDefault_text(verilogPreprocParser::Default_textContext *context) = 0;

    virtual antlrcpp::Any visitConditional(verilogPreprocParser::ConditionalContext *context) = 0;

    virtual antlrcpp::Any visitIfdef_directive(verilogPreprocParser::Ifdef_directiveContext *context) = 0;

    virtual antlrcpp::Any visitIfndef_directive(verilogPreprocParser::Ifndef_directiveContext *context) = 0;

    virtual antlrcpp::Any visitElse_group_of_lines(verilogPreprocParser::Else_group_of_linesContext *context) = 0;

    virtual antlrcpp::Any visitGroup_of_lines(verilogPreprocParser::Group_of_linesContext *context) = 0;

    virtual antlrcpp::Any visitMacro_call(verilogPreprocParser::Macro_callContext *context) = 0;

    virtual antlrcpp::Any visitValue(verilogPreprocParser::ValueContext *context) = 0;

    virtual antlrcpp::Any visitMacro_id(verilogPreprocParser::Macro_idContext *context) = 0;

    virtual antlrcpp::Any visitVar_id(verilogPreprocParser::Var_idContext *context) = 0;

    virtual antlrcpp::Any visitCond_id(verilogPreprocParser::Cond_idContext *context) = 0;

    virtual antlrcpp::Any visitUndef(verilogPreprocParser::UndefContext *context) = 0;

    virtual antlrcpp::Any visitCelldefine(verilogPreprocParser::CelldefineContext *context) = 0;

    virtual antlrcpp::Any visitEndcelldefine(verilogPreprocParser::EndcelldefineContext *context) = 0;

    virtual antlrcpp::Any visitUnconnected_drive(verilogPreprocParser::Unconnected_driveContext *context) = 0;

    virtual antlrcpp::Any visitNounconnected_drive(verilogPreprocParser::Nounconnected_driveContext *context) = 0;

    virtual antlrcpp::Any visitDefault_nettype(verilogPreprocParser::Default_nettypeContext *context) = 0;

    virtual antlrcpp::Any visitDefault_nettype_value(verilogPreprocParser::Default_nettype_valueContext *context) = 0;

    virtual antlrcpp::Any visitLine_directive(verilogPreprocParser::Line_directiveContext *context) = 0;

    virtual antlrcpp::Any visitTiming_spec(verilogPreprocParser::Timing_specContext *context) = 0;

    virtual antlrcpp::Any visitProtected_block(verilogPreprocParser::Protected_blockContext *context) = 0;

    virtual antlrcpp::Any visitResetall(verilogPreprocParser::ResetallContext *context) = 0;

    virtual antlrcpp::Any visitUndefineall(verilogPreprocParser::UndefineallContext *context) = 0;

    virtual antlrcpp::Any visitKeywords_directive(verilogPreprocParser::Keywords_directiveContext *context) = 0;

    virtual antlrcpp::Any visitVersion_specifier(verilogPreprocParser::Version_specifierContext *context) = 0;

    virtual antlrcpp::Any visitEndkeywords_directive(verilogPreprocParser::Endkeywords_directiveContext *context) = 0;

    virtual antlrcpp::Any visitInclude(verilogPreprocParser::IncludeContext *context) = 0;

    virtual antlrcpp::Any visitPragma(verilogPreprocParser::PragmaContext *context) = 0;

    virtual antlrcpp::Any visitPragma_name(verilogPreprocParser::Pragma_nameContext *context) = 0;

    virtual antlrcpp::Any visitPragma_expression(verilogPreprocParser::Pragma_expressionContext *context) = 0;

    virtual antlrcpp::Any visitPragma_value(verilogPreprocParser::Pragma_valueContext *context) = 0;

    virtual antlrcpp::Any visitPragma_keyword(verilogPreprocParser::Pragma_keywordContext *context) = 0;


};

}  // namespace verilogPreproc_antlr
