

#include <hdlConvertor/language.h>



// Generated from /home/circleci/project/grammars/verilogPreprocParser.g4 by ANTLR 4.7.2


#include "verilogPreprocParserVisitor.h"

#include "verilogPreprocParser.h"


using namespace antlrcpp;
using namespace verilogPreproc_antlr;
using namespace antlr4;

verilogPreprocParser::verilogPreprocParser(TokenStream *input) : Parser(input) {
  _interpreter = new atn::ParserATNSimulator(this, _atn, _decisionToDFA, _sharedContextCache);
}

verilogPreprocParser::~verilogPreprocParser() {
  delete _interpreter;
}

std::string verilogPreprocParser::getGrammarFileName() const {
  return "verilogPreprocParser.g4";
}

const std::vector<std::string>& verilogPreprocParser::getRuleNames() const {
  return _ruleNames;
}

dfa::Vocabulary& verilogPreprocParser::getVocabulary() const {
  return _vocabulary;
}


//----------------- FileContext ------------------------------------------------------------------

verilogPreprocParser::FileContext::FileContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::FileContext::EOF() {
  return getToken(verilogPreprocParser::EOF, 0);
}

std::vector<verilogPreprocParser::TextContext *> verilogPreprocParser::FileContext::text() {
  return getRuleContexts<verilogPreprocParser::TextContext>();
}

verilogPreprocParser::TextContext* verilogPreprocParser::FileContext::text(size_t i) {
  return getRuleContext<verilogPreprocParser::TextContext>(i);
}


size_t verilogPreprocParser::FileContext::getRuleIndex() const {
  return verilogPreprocParser::RuleFile;
}

antlrcpp::Any verilogPreprocParser::FileContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitFile(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::FileContext* verilogPreprocParser::file() {
  FileContext *_localctx = _tracker.createInstance<FileContext>(_ctx, getState());
  enterRule(_localctx, 0, verilogPreprocParser::RuleFile);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(85);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 0, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(82);
        text(); 
      }
      setState(87);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 0, _ctx);
    }
    setState(88);
    match(verilogPreprocParser::EOF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TextContext ------------------------------------------------------------------

verilogPreprocParser::TextContext::TextContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

verilogPreprocParser::Preprocess_directiveContext* verilogPreprocParser::TextContext::preprocess_directive() {
  return getRuleContext<verilogPreprocParser::Preprocess_directiveContext>(0);
}

tree::TerminalNode* verilogPreprocParser::TextContext::LINE_COMMENT() {
  return getToken(verilogPreprocParser::LINE_COMMENT, 0);
}

tree::TerminalNode* verilogPreprocParser::TextContext::CODE() {
  return getToken(verilogPreprocParser::CODE, 0);
}

tree::TerminalNode* verilogPreprocParser::TextContext::NEW_LINE() {
  return getToken(verilogPreprocParser::NEW_LINE, 0);
}

tree::TerminalNode* verilogPreprocParser::TextContext::NUM() {
  return getToken(verilogPreprocParser::NUM, 0);
}

tree::TerminalNode* verilogPreprocParser::TextContext::ID() {
  return getToken(verilogPreprocParser::ID, 0);
}

tree::TerminalNode* verilogPreprocParser::TextContext::STR() {
  return getToken(verilogPreprocParser::STR, 0);
}

tree::TerminalNode* verilogPreprocParser::TextContext::COMMENT() {
  return getToken(verilogPreprocParser::COMMENT, 0);
}


size_t verilogPreprocParser::TextContext::getRuleIndex() const {
  return verilogPreprocParser::RuleText;
}

antlrcpp::Any verilogPreprocParser::TextContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitText(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::TextContext* verilogPreprocParser::text() {
  TextContext *_localctx = _tracker.createInstance<TextContext>(_ctx, getState());
  enterRule(_localctx, 2, verilogPreprocParser::RuleText);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    setState(99);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 1, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(90);
      preprocess_directive();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(91);
      match(verilogPreprocParser::LINE_COMMENT);
      break;
    }

    case 3: {
      enterOuterAlt(_localctx, 3);
      setState(92);
      match(verilogPreprocParser::CODE);
      break;
    }

    case 4: {
      enterOuterAlt(_localctx, 4);
      setState(93);
      match(verilogPreprocParser::NEW_LINE);
      break;
    }

    case 5: {
      enterOuterAlt(_localctx, 5);
      setState(94);
      match(verilogPreprocParser::NUM);
      break;
    }

    case 6: {
      enterOuterAlt(_localctx, 6);
      setState(95);
      match(verilogPreprocParser::ID);
      break;
    }

    case 7: {
      enterOuterAlt(_localctx, 7);
      setState(96);
      match(verilogPreprocParser::STR);
      break;
    }

    case 8: {
      enterOuterAlt(_localctx, 8);
      setState(97);
      match(verilogPreprocParser::NEW_LINE);
      break;
    }

    case 9: {
      enterOuterAlt(_localctx, 9);
      setState(98);
      match(verilogPreprocParser::COMMENT);
      break;
    }

    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Preprocess_directiveContext ------------------------------------------------------------------

verilogPreprocParser::Preprocess_directiveContext::Preprocess_directiveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

verilogPreprocParser::DefineContext* verilogPreprocParser::Preprocess_directiveContext::define() {
  return getRuleContext<verilogPreprocParser::DefineContext>(0);
}

verilogPreprocParser::ConditionalContext* verilogPreprocParser::Preprocess_directiveContext::conditional() {
  return getRuleContext<verilogPreprocParser::ConditionalContext>(0);
}

verilogPreprocParser::Macro_callContext* verilogPreprocParser::Preprocess_directiveContext::macro_call() {
  return getRuleContext<verilogPreprocParser::Macro_callContext>(0);
}

verilogPreprocParser::ResetallContext* verilogPreprocParser::Preprocess_directiveContext::resetall() {
  return getRuleContext<verilogPreprocParser::ResetallContext>(0);
}

verilogPreprocParser::UndefContext* verilogPreprocParser::Preprocess_directiveContext::undef() {
  return getRuleContext<verilogPreprocParser::UndefContext>(0);
}

verilogPreprocParser::IncludeContext* verilogPreprocParser::Preprocess_directiveContext::include() {
  return getRuleContext<verilogPreprocParser::IncludeContext>(0);
}

verilogPreprocParser::CelldefineContext* verilogPreprocParser::Preprocess_directiveContext::celldefine() {
  return getRuleContext<verilogPreprocParser::CelldefineContext>(0);
}

verilogPreprocParser::EndcelldefineContext* verilogPreprocParser::Preprocess_directiveContext::endcelldefine() {
  return getRuleContext<verilogPreprocParser::EndcelldefineContext>(0);
}

verilogPreprocParser::Unconnected_driveContext* verilogPreprocParser::Preprocess_directiveContext::unconnected_drive() {
  return getRuleContext<verilogPreprocParser::Unconnected_driveContext>(0);
}

verilogPreprocParser::Nounconnected_driveContext* verilogPreprocParser::Preprocess_directiveContext::nounconnected_drive() {
  return getRuleContext<verilogPreprocParser::Nounconnected_driveContext>(0);
}

verilogPreprocParser::Default_nettypeContext* verilogPreprocParser::Preprocess_directiveContext::default_nettype() {
  return getRuleContext<verilogPreprocParser::Default_nettypeContext>(0);
}

verilogPreprocParser::Line_directiveContext* verilogPreprocParser::Preprocess_directiveContext::line_directive() {
  return getRuleContext<verilogPreprocParser::Line_directiveContext>(0);
}

verilogPreprocParser::Timing_specContext* verilogPreprocParser::Preprocess_directiveContext::timing_spec() {
  return getRuleContext<verilogPreprocParser::Timing_specContext>(0);
}

verilogPreprocParser::Protected_blockContext* verilogPreprocParser::Preprocess_directiveContext::protected_block() {
  return getRuleContext<verilogPreprocParser::Protected_blockContext>(0);
}

verilogPreprocParser::UndefineallContext* verilogPreprocParser::Preprocess_directiveContext::undefineall() {
  return getRuleContext<verilogPreprocParser::UndefineallContext>(0);
}

verilogPreprocParser::Keywords_directiveContext* verilogPreprocParser::Preprocess_directiveContext::keywords_directive() {
  return getRuleContext<verilogPreprocParser::Keywords_directiveContext>(0);
}

verilogPreprocParser::Endkeywords_directiveContext* verilogPreprocParser::Preprocess_directiveContext::endkeywords_directive() {
  return getRuleContext<verilogPreprocParser::Endkeywords_directiveContext>(0);
}

verilogPreprocParser::PragmaContext* verilogPreprocParser::Preprocess_directiveContext::pragma() {
  return getRuleContext<verilogPreprocParser::PragmaContext>(0);
}


size_t verilogPreprocParser::Preprocess_directiveContext::getRuleIndex() const {
  return verilogPreprocParser::RulePreprocess_directive;
}

antlrcpp::Any verilogPreprocParser::Preprocess_directiveContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitPreprocess_directive(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Preprocess_directiveContext* verilogPreprocParser::preprocess_directive() {
  Preprocess_directiveContext *_localctx = _tracker.createInstance<Preprocess_directiveContext>(_ctx, getState());
  enterRule(_localctx, 4, verilogPreprocParser::RulePreprocess_directive);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    setState(123);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 3, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(101);
      define();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(102);
      conditional();
      break;
    }

    case 3: {
      enterOuterAlt(_localctx, 3);
      setState(103);
      macro_call();
      break;
    }

    case 4: {
      enterOuterAlt(_localctx, 4);
      setState(104);
      resetall();
      break;
    }

    case 5: {
      enterOuterAlt(_localctx, 5);
      setState(105);
      undef();
      break;
    }

    case 6: {
      enterOuterAlt(_localctx, 6);
      setState(106);
      include();
      break;
    }

    case 7: {
      enterOuterAlt(_localctx, 7);
      setState(107);
      celldefine();
      break;
    }

    case 8: {
      enterOuterAlt(_localctx, 8);
      setState(108);
      endcelldefine();
      break;
    }

    case 9: {
      enterOuterAlt(_localctx, 9);
      setState(109);
      unconnected_drive();
      break;
    }

    case 10: {
      enterOuterAlt(_localctx, 10);
      setState(110);
      nounconnected_drive();
      break;
    }

    case 11: {
      enterOuterAlt(_localctx, 11);
      setState(111);
      default_nettype();
      break;
    }

    case 12: {
      enterOuterAlt(_localctx, 12);
      setState(112);
      line_directive();
      break;
    }

    case 13: {
      enterOuterAlt(_localctx, 13);
      setState(113);
      timing_spec();
      break;
    }

    case 14: {
      enterOuterAlt(_localctx, 14);
      setState(114);
      protected_block();
      break;
    }

    case 15: {
      enterOuterAlt(_localctx, 15);
      setState(115);

      if (!(language_version >= hdlConvertor::Language::SV2009)) throw FailedPredicateException(this, "language_version >= hdlConvertor::Language::SV2009");
      setState(116);
      undefineall();
      break;
    }

    case 16: {
      enterOuterAlt(_localctx, 16);
      setState(117);

      if (!(language_version >= hdlConvertor::Language::VERILOG2005)) throw FailedPredicateException(this, "language_version >= hdlConvertor::Language::VERILOG2005");
      setState(121);
      _errHandler->sync(this);
      switch (_input->LA(1)) {
        case verilogPreprocParser::BEGIN_KEYWORDS: {
          setState(118);
          keywords_directive();
          break;
        }

        case verilogPreprocParser::END_KEYWORDS: {
          setState(119);
          endkeywords_directive();
          break;
        }

        case verilogPreprocParser::PRAGMA: {
          setState(120);
          pragma();
          break;
        }

      default:
        throw NoViableAltException(this);
      }
      break;
    }

    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- DefineContext ------------------------------------------------------------------

verilogPreprocParser::DefineContext::DefineContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::DefineContext::DEFINE() {
  return getToken(verilogPreprocParser::DEFINE, 0);
}

verilogPreprocParser::Macro_idContext* verilogPreprocParser::DefineContext::macro_id() {
  return getRuleContext<verilogPreprocParser::Macro_idContext>(0);
}

tree::TerminalNode* verilogPreprocParser::DefineContext::LINE_COMMENT() {
  return getToken(verilogPreprocParser::LINE_COMMENT, 0);
}

tree::TerminalNode* verilogPreprocParser::DefineContext::NEW_LINE() {
  return getToken(verilogPreprocParser::NEW_LINE, 0);
}

tree::TerminalNode* verilogPreprocParser::DefineContext::EOF() {
  return getToken(verilogPreprocParser::EOF, 0);
}

tree::TerminalNode* verilogPreprocParser::DefineContext::LP() {
  return getToken(verilogPreprocParser::LP, 0);
}

tree::TerminalNode* verilogPreprocParser::DefineContext::RP() {
  return getToken(verilogPreprocParser::RP, 0);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::DefineContext::WS() {
  return getTokens(verilogPreprocParser::WS);
}

tree::TerminalNode* verilogPreprocParser::DefineContext::WS(size_t i) {
  return getToken(verilogPreprocParser::WS, i);
}

verilogPreprocParser::ReplacementContext* verilogPreprocParser::DefineContext::replacement() {
  return getRuleContext<verilogPreprocParser::ReplacementContext>(0);
}

verilogPreprocParser::Define_argsContext* verilogPreprocParser::DefineContext::define_args() {
  return getRuleContext<verilogPreprocParser::Define_argsContext>(0);
}


size_t verilogPreprocParser::DefineContext::getRuleIndex() const {
  return verilogPreprocParser::RuleDefine;
}

antlrcpp::Any verilogPreprocParser::DefineContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitDefine(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::DefineContext* verilogPreprocParser::define() {
  DefineContext *_localctx = _tracker.createInstance<DefineContext>(_ctx, getState());
  enterRule(_localctx, 6, verilogPreprocParser::RuleDefine);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(125);
    match(verilogPreprocParser::DEFINE);
    setState(126);
    macro_id();
    setState(132);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == verilogPreprocParser::LP) {
      setState(127);
      match(verilogPreprocParser::LP);
      setState(129);
      _errHandler->sync(this);

      switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 4, _ctx)) {
      case 1: {
        setState(128);
        define_args();
        break;
      }

      }
      setState(131);
      match(verilogPreprocParser::RP);
    }
    setState(137);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == verilogPreprocParser::WS) {
      setState(134);
      match(verilogPreprocParser::WS);
      setState(139);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(141);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == verilogPreprocParser::CODE) {
      setState(140);
      replacement();
    }
    setState(143);
    _la = _input->LA(1);
    if (!(((((_la - -1) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - -1)) & ((1ULL << (verilogPreprocParser::EOF - -1))
      | (1ULL << (verilogPreprocParser::LINE_COMMENT - -1))
      | (1ULL << (verilogPreprocParser::NEW_LINE - -1)))) != 0))) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Define_argsContext ------------------------------------------------------------------

verilogPreprocParser::Define_argsContext::Define_argsContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

verilogPreprocParser::Define_args_with_def_valContext* verilogPreprocParser::Define_argsContext::define_args_with_def_val() {
  return getRuleContext<verilogPreprocParser::Define_args_with_def_valContext>(0);
}

verilogPreprocParser::Define_args_basicContext* verilogPreprocParser::Define_argsContext::define_args_basic() {
  return getRuleContext<verilogPreprocParser::Define_args_basicContext>(0);
}


size_t verilogPreprocParser::Define_argsContext::getRuleIndex() const {
  return verilogPreprocParser::RuleDefine_args;
}

antlrcpp::Any verilogPreprocParser::Define_argsContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitDefine_args(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Define_argsContext* verilogPreprocParser::define_args() {
  Define_argsContext *_localctx = _tracker.createInstance<Define_argsContext>(_ctx, getState());
  enterRule(_localctx, 8, verilogPreprocParser::RuleDefine_args);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    setState(149);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 8, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(145);

      if (!( language_version >= hdlConvertor::Language::SV2009 )) throw FailedPredicateException(this, " language_version >= hdlConvertor::Language::SV2009 ");
      setState(146);
      define_args_with_def_val();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(147);

      if (!( language_version < hdlConvertor::Language::SV2009 )) throw FailedPredicateException(this, " language_version < hdlConvertor::Language::SV2009 ");
      setState(148);
      define_args_basic();
      break;
    }

    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Define_args_with_def_valContext ------------------------------------------------------------------

verilogPreprocParser::Define_args_with_def_valContext::Define_args_with_def_valContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<verilogPreprocParser::Param_with_def_valContext *> verilogPreprocParser::Define_args_with_def_valContext::param_with_def_val() {
  return getRuleContexts<verilogPreprocParser::Param_with_def_valContext>();
}

verilogPreprocParser::Param_with_def_valContext* verilogPreprocParser::Define_args_with_def_valContext::param_with_def_val(size_t i) {
  return getRuleContext<verilogPreprocParser::Param_with_def_valContext>(i);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::Define_args_with_def_valContext::COMMA() {
  return getTokens(verilogPreprocParser::COMMA);
}

tree::TerminalNode* verilogPreprocParser::Define_args_with_def_valContext::COMMA(size_t i) {
  return getToken(verilogPreprocParser::COMMA, i);
}


size_t verilogPreprocParser::Define_args_with_def_valContext::getRuleIndex() const {
  return verilogPreprocParser::RuleDefine_args_with_def_val;
}

antlrcpp::Any verilogPreprocParser::Define_args_with_def_valContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitDefine_args_with_def_val(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Define_args_with_def_valContext* verilogPreprocParser::define_args_with_def_val() {
  Define_args_with_def_valContext *_localctx = _tracker.createInstance<Define_args_with_def_valContext>(_ctx, getState());
  enterRule(_localctx, 10, verilogPreprocParser::RuleDefine_args_with_def_val);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(151);
    param_with_def_val();
    setState(156);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == verilogPreprocParser::COMMA) {
      setState(152);
      match(verilogPreprocParser::COMMA);
      setState(153);
      param_with_def_val();
      setState(158);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Param_with_def_valContext ------------------------------------------------------------------

verilogPreprocParser::Param_with_def_valContext::Param_with_def_valContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

verilogPreprocParser::Var_idContext* verilogPreprocParser::Param_with_def_valContext::var_id() {
  return getRuleContext<verilogPreprocParser::Var_idContext>(0);
}

tree::TerminalNode* verilogPreprocParser::Param_with_def_valContext::EQUAL() {
  return getToken(verilogPreprocParser::EQUAL, 0);
}

verilogPreprocParser::Default_textContext* verilogPreprocParser::Param_with_def_valContext::default_text() {
  return getRuleContext<verilogPreprocParser::Default_textContext>(0);
}


size_t verilogPreprocParser::Param_with_def_valContext::getRuleIndex() const {
  return verilogPreprocParser::RuleParam_with_def_val;
}

antlrcpp::Any verilogPreprocParser::Param_with_def_valContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitParam_with_def_val(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Param_with_def_valContext* verilogPreprocParser::param_with_def_val() {
  Param_with_def_valContext *_localctx = _tracker.createInstance<Param_with_def_valContext>(_ctx, getState());
  enterRule(_localctx, 12, verilogPreprocParser::RuleParam_with_def_val);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(159);
    var_id();
    setState(164);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == verilogPreprocParser::EQUAL) {
      setState(160);
      match(verilogPreprocParser::EQUAL);
      setState(162);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if (_la == verilogPreprocParser::CODE) {
        setState(161);
        default_text();
      }
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Define_args_basicContext ------------------------------------------------------------------

verilogPreprocParser::Define_args_basicContext::Define_args_basicContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<verilogPreprocParser::Var_idContext *> verilogPreprocParser::Define_args_basicContext::var_id() {
  return getRuleContexts<verilogPreprocParser::Var_idContext>();
}

verilogPreprocParser::Var_idContext* verilogPreprocParser::Define_args_basicContext::var_id(size_t i) {
  return getRuleContext<verilogPreprocParser::Var_idContext>(i);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::Define_args_basicContext::COMMA() {
  return getTokens(verilogPreprocParser::COMMA);
}

tree::TerminalNode* verilogPreprocParser::Define_args_basicContext::COMMA(size_t i) {
  return getToken(verilogPreprocParser::COMMA, i);
}


size_t verilogPreprocParser::Define_args_basicContext::getRuleIndex() const {
  return verilogPreprocParser::RuleDefine_args_basic;
}

antlrcpp::Any verilogPreprocParser::Define_args_basicContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitDefine_args_basic(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Define_args_basicContext* verilogPreprocParser::define_args_basic() {
  Define_args_basicContext *_localctx = _tracker.createInstance<Define_args_basicContext>(_ctx, getState());
  enterRule(_localctx, 14, verilogPreprocParser::RuleDefine_args_basic);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(166);
    var_id();
    setState(171);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == verilogPreprocParser::COMMA) {
      setState(167);
      match(verilogPreprocParser::COMMA);
      setState(168);
      var_id();
      setState(173);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ReplacementContext ------------------------------------------------------------------

verilogPreprocParser::ReplacementContext::ReplacementContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> verilogPreprocParser::ReplacementContext::CODE() {
  return getTokens(verilogPreprocParser::CODE);
}

tree::TerminalNode* verilogPreprocParser::ReplacementContext::CODE(size_t i) {
  return getToken(verilogPreprocParser::CODE, i);
}


size_t verilogPreprocParser::ReplacementContext::getRuleIndex() const {
  return verilogPreprocParser::RuleReplacement;
}

antlrcpp::Any verilogPreprocParser::ReplacementContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitReplacement(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::ReplacementContext* verilogPreprocParser::replacement() {
  ReplacementContext *_localctx = _tracker.createInstance<ReplacementContext>(_ctx, getState());
  enterRule(_localctx, 16, verilogPreprocParser::RuleReplacement);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(175); 
    _errHandler->sync(this);
    _la = _input->LA(1);
    do {
      setState(174);
      match(verilogPreprocParser::CODE);
      setState(177); 
      _errHandler->sync(this);
      _la = _input->LA(1);
    } while (_la == verilogPreprocParser::CODE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Default_textContext ------------------------------------------------------------------

verilogPreprocParser::Default_textContext::Default_textContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> verilogPreprocParser::Default_textContext::CODE() {
  return getTokens(verilogPreprocParser::CODE);
}

tree::TerminalNode* verilogPreprocParser::Default_textContext::CODE(size_t i) {
  return getToken(verilogPreprocParser::CODE, i);
}


size_t verilogPreprocParser::Default_textContext::getRuleIndex() const {
  return verilogPreprocParser::RuleDefault_text;
}

antlrcpp::Any verilogPreprocParser::Default_textContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitDefault_text(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Default_textContext* verilogPreprocParser::default_text() {
  Default_textContext *_localctx = _tracker.createInstance<Default_textContext>(_ctx, getState());
  enterRule(_localctx, 18, verilogPreprocParser::RuleDefault_text);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(180); 
    _errHandler->sync(this);
    _la = _input->LA(1);
    do {
      setState(179);
      match(verilogPreprocParser::CODE);
      setState(182); 
      _errHandler->sync(this);
      _la = _input->LA(1);
    } while (_la == verilogPreprocParser::CODE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ConditionalContext ------------------------------------------------------------------

verilogPreprocParser::ConditionalContext::ConditionalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

verilogPreprocParser::Ifdef_directiveContext* verilogPreprocParser::ConditionalContext::ifdef_directive() {
  return getRuleContext<verilogPreprocParser::Ifdef_directiveContext>(0);
}

verilogPreprocParser::Ifndef_directiveContext* verilogPreprocParser::ConditionalContext::ifndef_directive() {
  return getRuleContext<verilogPreprocParser::Ifndef_directiveContext>(0);
}


size_t verilogPreprocParser::ConditionalContext::getRuleIndex() const {
  return verilogPreprocParser::RuleConditional;
}

antlrcpp::Any verilogPreprocParser::ConditionalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitConditional(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::ConditionalContext* verilogPreprocParser::conditional() {
  ConditionalContext *_localctx = _tracker.createInstance<ConditionalContext>(_ctx, getState());
  enterRule(_localctx, 20, verilogPreprocParser::RuleConditional);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    setState(186);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case verilogPreprocParser::IFDEF: {
        enterOuterAlt(_localctx, 1);
        setState(184);
        ifdef_directive();
        break;
      }

      case verilogPreprocParser::IFNDEF: {
        enterOuterAlt(_localctx, 2);
        setState(185);
        ifndef_directive();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Ifdef_directiveContext ------------------------------------------------------------------

verilogPreprocParser::Ifdef_directiveContext::Ifdef_directiveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Ifdef_directiveContext::IFDEF() {
  return getToken(verilogPreprocParser::IFDEF, 0);
}

std::vector<verilogPreprocParser::Cond_idContext *> verilogPreprocParser::Ifdef_directiveContext::cond_id() {
  return getRuleContexts<verilogPreprocParser::Cond_idContext>();
}

verilogPreprocParser::Cond_idContext* verilogPreprocParser::Ifdef_directiveContext::cond_id(size_t i) {
  return getRuleContext<verilogPreprocParser::Cond_idContext>(i);
}

std::vector<verilogPreprocParser::Group_of_linesContext *> verilogPreprocParser::Ifdef_directiveContext::group_of_lines() {
  return getRuleContexts<verilogPreprocParser::Group_of_linesContext>();
}

verilogPreprocParser::Group_of_linesContext* verilogPreprocParser::Ifdef_directiveContext::group_of_lines(size_t i) {
  return getRuleContext<verilogPreprocParser::Group_of_linesContext>(i);
}

tree::TerminalNode* verilogPreprocParser::Ifdef_directiveContext::ENDIF() {
  return getToken(verilogPreprocParser::ENDIF, 0);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::Ifdef_directiveContext::ELSIF() {
  return getTokens(verilogPreprocParser::ELSIF);
}

tree::TerminalNode* verilogPreprocParser::Ifdef_directiveContext::ELSIF(size_t i) {
  return getToken(verilogPreprocParser::ELSIF, i);
}

tree::TerminalNode* verilogPreprocParser::Ifdef_directiveContext::ELSE() {
  return getToken(verilogPreprocParser::ELSE, 0);
}

verilogPreprocParser::Else_group_of_linesContext* verilogPreprocParser::Ifdef_directiveContext::else_group_of_lines() {
  return getRuleContext<verilogPreprocParser::Else_group_of_linesContext>(0);
}


size_t verilogPreprocParser::Ifdef_directiveContext::getRuleIndex() const {
  return verilogPreprocParser::RuleIfdef_directive;
}

antlrcpp::Any verilogPreprocParser::Ifdef_directiveContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitIfdef_directive(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Ifdef_directiveContext* verilogPreprocParser::ifdef_directive() {
  Ifdef_directiveContext *_localctx = _tracker.createInstance<Ifdef_directiveContext>(_ctx, getState());
  enterRule(_localctx, 22, verilogPreprocParser::RuleIfdef_directive);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(188);
    match(verilogPreprocParser::IFDEF);
    setState(189);
    cond_id();
    setState(190);
    group_of_lines();
    setState(197);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == verilogPreprocParser::ELSIF) {
      setState(191);
      match(verilogPreprocParser::ELSIF);
      setState(192);
      cond_id();
      setState(193);
      group_of_lines();
      setState(199);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(202);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == verilogPreprocParser::ELSE) {
      setState(200);
      match(verilogPreprocParser::ELSE);
      setState(201);
      else_group_of_lines();
    }
    setState(204);
    match(verilogPreprocParser::ENDIF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Ifndef_directiveContext ------------------------------------------------------------------

verilogPreprocParser::Ifndef_directiveContext::Ifndef_directiveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Ifndef_directiveContext::IFNDEF() {
  return getToken(verilogPreprocParser::IFNDEF, 0);
}

std::vector<verilogPreprocParser::Cond_idContext *> verilogPreprocParser::Ifndef_directiveContext::cond_id() {
  return getRuleContexts<verilogPreprocParser::Cond_idContext>();
}

verilogPreprocParser::Cond_idContext* verilogPreprocParser::Ifndef_directiveContext::cond_id(size_t i) {
  return getRuleContext<verilogPreprocParser::Cond_idContext>(i);
}

std::vector<verilogPreprocParser::Group_of_linesContext *> verilogPreprocParser::Ifndef_directiveContext::group_of_lines() {
  return getRuleContexts<verilogPreprocParser::Group_of_linesContext>();
}

verilogPreprocParser::Group_of_linesContext* verilogPreprocParser::Ifndef_directiveContext::group_of_lines(size_t i) {
  return getRuleContext<verilogPreprocParser::Group_of_linesContext>(i);
}

tree::TerminalNode* verilogPreprocParser::Ifndef_directiveContext::ENDIF() {
  return getToken(verilogPreprocParser::ENDIF, 0);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::Ifndef_directiveContext::ELSIF() {
  return getTokens(verilogPreprocParser::ELSIF);
}

tree::TerminalNode* verilogPreprocParser::Ifndef_directiveContext::ELSIF(size_t i) {
  return getToken(verilogPreprocParser::ELSIF, i);
}

tree::TerminalNode* verilogPreprocParser::Ifndef_directiveContext::ELSE() {
  return getToken(verilogPreprocParser::ELSE, 0);
}

verilogPreprocParser::Else_group_of_linesContext* verilogPreprocParser::Ifndef_directiveContext::else_group_of_lines() {
  return getRuleContext<verilogPreprocParser::Else_group_of_linesContext>(0);
}


size_t verilogPreprocParser::Ifndef_directiveContext::getRuleIndex() const {
  return verilogPreprocParser::RuleIfndef_directive;
}

antlrcpp::Any verilogPreprocParser::Ifndef_directiveContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitIfndef_directive(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Ifndef_directiveContext* verilogPreprocParser::ifndef_directive() {
  Ifndef_directiveContext *_localctx = _tracker.createInstance<Ifndef_directiveContext>(_ctx, getState());
  enterRule(_localctx, 24, verilogPreprocParser::RuleIfndef_directive);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(206);
    match(verilogPreprocParser::IFNDEF);
    setState(207);
    cond_id();
    setState(208);
    group_of_lines();
    setState(215);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == verilogPreprocParser::ELSIF) {
      setState(209);
      match(verilogPreprocParser::ELSIF);
      setState(210);
      cond_id();
      setState(211);
      group_of_lines();
      setState(217);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(220);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == verilogPreprocParser::ELSE) {
      setState(218);
      match(verilogPreprocParser::ELSE);
      setState(219);
      else_group_of_lines();
    }
    setState(222);
    match(verilogPreprocParser::ENDIF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Else_group_of_linesContext ------------------------------------------------------------------

verilogPreprocParser::Else_group_of_linesContext::Else_group_of_linesContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

verilogPreprocParser::Group_of_linesContext* verilogPreprocParser::Else_group_of_linesContext::group_of_lines() {
  return getRuleContext<verilogPreprocParser::Group_of_linesContext>(0);
}


size_t verilogPreprocParser::Else_group_of_linesContext::getRuleIndex() const {
  return verilogPreprocParser::RuleElse_group_of_lines;
}

antlrcpp::Any verilogPreprocParser::Else_group_of_linesContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitElse_group_of_lines(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Else_group_of_linesContext* verilogPreprocParser::else_group_of_lines() {
  Else_group_of_linesContext *_localctx = _tracker.createInstance<Else_group_of_linesContext>(_ctx, getState());
  enterRule(_localctx, 26, verilogPreprocParser::RuleElse_group_of_lines);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(224);
    group_of_lines();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Group_of_linesContext ------------------------------------------------------------------

verilogPreprocParser::Group_of_linesContext::Group_of_linesContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<verilogPreprocParser::TextContext *> verilogPreprocParser::Group_of_linesContext::text() {
  return getRuleContexts<verilogPreprocParser::TextContext>();
}

verilogPreprocParser::TextContext* verilogPreprocParser::Group_of_linesContext::text(size_t i) {
  return getRuleContext<verilogPreprocParser::TextContext>(i);
}


size_t verilogPreprocParser::Group_of_linesContext::getRuleIndex() const {
  return verilogPreprocParser::RuleGroup_of_lines;
}

antlrcpp::Any verilogPreprocParser::Group_of_linesContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitGroup_of_lines(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Group_of_linesContext* verilogPreprocParser::group_of_lines() {
  Group_of_linesContext *_localctx = _tracker.createInstance<Group_of_linesContext>(_ctx, getState());
  enterRule(_localctx, 28, verilogPreprocParser::RuleGroup_of_lines);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(229);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 20, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        setState(226);
        text(); 
      }
      setState(231);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 20, _ctx);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Macro_callContext ------------------------------------------------------------------

verilogPreprocParser::Macro_callContext::Macro_callContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Macro_callContext::OTHER_MACRO_CALL_NO_ARGS() {
  return getToken(verilogPreprocParser::OTHER_MACRO_CALL_NO_ARGS, 0);
}

tree::TerminalNode* verilogPreprocParser::Macro_callContext::OTHER_MACRO_CALL_WITH_ARGS() {
  return getToken(verilogPreprocParser::OTHER_MACRO_CALL_WITH_ARGS, 0);
}

tree::TerminalNode* verilogPreprocParser::Macro_callContext::RP() {
  return getToken(verilogPreprocParser::RP, 0);
}

std::vector<verilogPreprocParser::ValueContext *> verilogPreprocParser::Macro_callContext::value() {
  return getRuleContexts<verilogPreprocParser::ValueContext>();
}

verilogPreprocParser::ValueContext* verilogPreprocParser::Macro_callContext::value(size_t i) {
  return getRuleContext<verilogPreprocParser::ValueContext>(i);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::Macro_callContext::COMMA() {
  return getTokens(verilogPreprocParser::COMMA);
}

tree::TerminalNode* verilogPreprocParser::Macro_callContext::COMMA(size_t i) {
  return getToken(verilogPreprocParser::COMMA, i);
}


size_t verilogPreprocParser::Macro_callContext::getRuleIndex() const {
  return verilogPreprocParser::RuleMacro_call;
}

antlrcpp::Any verilogPreprocParser::Macro_callContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitMacro_call(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Macro_callContext* verilogPreprocParser::macro_call() {
  Macro_callContext *_localctx = _tracker.createInstance<Macro_callContext>(_ctx, getState());
  enterRule(_localctx, 30, verilogPreprocParser::RuleMacro_call);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    setState(247);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case verilogPreprocParser::OTHER_MACRO_CALL_NO_ARGS: {
        enterOuterAlt(_localctx, 1);
        setState(232);
        match(verilogPreprocParser::OTHER_MACRO_CALL_NO_ARGS);
        break;
      }

      case verilogPreprocParser::OTHER_MACRO_CALL_WITH_ARGS: {
        enterOuterAlt(_localctx, 2);
        setState(233);
        match(verilogPreprocParser::OTHER_MACRO_CALL_WITH_ARGS);
        setState(235);
        _errHandler->sync(this);

        switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 21, _ctx)) {
        case 1: {
          setState(234);
          value();
          break;
        }

        }
        setState(243);
        _errHandler->sync(this);
        _la = _input->LA(1);
        while (_la == verilogPreprocParser::COMMA) {
          setState(237);
          match(verilogPreprocParser::COMMA);
          setState(239);
          _errHandler->sync(this);

          switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 22, _ctx)) {
          case 1: {
            setState(238);
            value();
            break;
          }

          }
          setState(245);
          _errHandler->sync(this);
          _la = _input->LA(1);
        }
        setState(246);
        match(verilogPreprocParser::RP);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ValueContext ------------------------------------------------------------------

verilogPreprocParser::ValueContext::ValueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<verilogPreprocParser::TextContext *> verilogPreprocParser::ValueContext::text() {
  return getRuleContexts<verilogPreprocParser::TextContext>();
}

verilogPreprocParser::TextContext* verilogPreprocParser::ValueContext::text(size_t i) {
  return getRuleContext<verilogPreprocParser::TextContext>(i);
}


size_t verilogPreprocParser::ValueContext::getRuleIndex() const {
  return verilogPreprocParser::RuleValue;
}

antlrcpp::Any verilogPreprocParser::ValueContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitValue(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::ValueContext* verilogPreprocParser::value() {
  ValueContext *_localctx = _tracker.createInstance<ValueContext>(_ctx, getState());
  enterRule(_localctx, 32, verilogPreprocParser::RuleValue);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(250); 
    _errHandler->sync(this);
    alt = 1;
    do {
      switch (alt) {
        case 1: {
              setState(249);
              text();
              break;
            }

      default:
        throw NoViableAltException(this);
      }
      setState(252); 
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 25, _ctx);
    } while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Macro_idContext ------------------------------------------------------------------

verilogPreprocParser::Macro_idContext::Macro_idContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Macro_idContext::ID() {
  return getToken(verilogPreprocParser::ID, 0);
}


size_t verilogPreprocParser::Macro_idContext::getRuleIndex() const {
  return verilogPreprocParser::RuleMacro_id;
}

antlrcpp::Any verilogPreprocParser::Macro_idContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitMacro_id(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Macro_idContext* verilogPreprocParser::macro_id() {
  Macro_idContext *_localctx = _tracker.createInstance<Macro_idContext>(_ctx, getState());
  enterRule(_localctx, 34, verilogPreprocParser::RuleMacro_id);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(254);
    match(verilogPreprocParser::ID);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Var_idContext ------------------------------------------------------------------

verilogPreprocParser::Var_idContext::Var_idContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Var_idContext::ID() {
  return getToken(verilogPreprocParser::ID, 0);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::Var_idContext::COMMENT() {
  return getTokens(verilogPreprocParser::COMMENT);
}

tree::TerminalNode* verilogPreprocParser::Var_idContext::COMMENT(size_t i) {
  return getToken(verilogPreprocParser::COMMENT, i);
}


size_t verilogPreprocParser::Var_idContext::getRuleIndex() const {
  return verilogPreprocParser::RuleVar_id;
}

antlrcpp::Any verilogPreprocParser::Var_idContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitVar_id(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Var_idContext* verilogPreprocParser::var_id() {
  Var_idContext *_localctx = _tracker.createInstance<Var_idContext>(_ctx, getState());
  enterRule(_localctx, 36, verilogPreprocParser::RuleVar_id);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(259);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == verilogPreprocParser::COMMENT) {
      setState(256);
      match(verilogPreprocParser::COMMENT);
      setState(261);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(262);
    match(verilogPreprocParser::ID);
    setState(266);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == verilogPreprocParser::COMMENT) {
      setState(263);
      match(verilogPreprocParser::COMMENT);
      setState(268);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Cond_idContext ------------------------------------------------------------------

verilogPreprocParser::Cond_idContext::Cond_idContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Cond_idContext::ID() {
  return getToken(verilogPreprocParser::ID, 0);
}


size_t verilogPreprocParser::Cond_idContext::getRuleIndex() const {
  return verilogPreprocParser::RuleCond_id;
}

antlrcpp::Any verilogPreprocParser::Cond_idContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitCond_id(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Cond_idContext* verilogPreprocParser::cond_id() {
  Cond_idContext *_localctx = _tracker.createInstance<Cond_idContext>(_ctx, getState());
  enterRule(_localctx, 38, verilogPreprocParser::RuleCond_id);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(269);
    match(verilogPreprocParser::ID);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- UndefContext ------------------------------------------------------------------

verilogPreprocParser::UndefContext::UndefContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::UndefContext::UNDEF() {
  return getToken(verilogPreprocParser::UNDEF, 0);
}

tree::TerminalNode* verilogPreprocParser::UndefContext::ID() {
  return getToken(verilogPreprocParser::ID, 0);
}

tree::TerminalNode* verilogPreprocParser::UndefContext::WS() {
  return getToken(verilogPreprocParser::WS, 0);
}

tree::TerminalNode* verilogPreprocParser::UndefContext::NEW_LINE() {
  return getToken(verilogPreprocParser::NEW_LINE, 0);
}

tree::TerminalNode* verilogPreprocParser::UndefContext::EOF() {
  return getToken(verilogPreprocParser::EOF, 0);
}


size_t verilogPreprocParser::UndefContext::getRuleIndex() const {
  return verilogPreprocParser::RuleUndef;
}

antlrcpp::Any verilogPreprocParser::UndefContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitUndef(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::UndefContext* verilogPreprocParser::undef() {
  UndefContext *_localctx = _tracker.createInstance<UndefContext>(_ctx, getState());
  enterRule(_localctx, 40, verilogPreprocParser::RuleUndef);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(271);
    match(verilogPreprocParser::UNDEF);
    setState(272);
    match(verilogPreprocParser::ID);
    setState(273);
    _la = _input->LA(1);
    if (!(((((_la - -1) & ~ 0x3fULL) == 0) &&
      ((1ULL << (_la - -1)) & ((1ULL << (verilogPreprocParser::EOF - -1))
      | (1ULL << (verilogPreprocParser::WS - -1))
      | (1ULL << (verilogPreprocParser::NEW_LINE - -1)))) != 0))) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- CelldefineContext ------------------------------------------------------------------

verilogPreprocParser::CelldefineContext::CelldefineContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::CelldefineContext::CELLDEFINE() {
  return getToken(verilogPreprocParser::CELLDEFINE, 0);
}


size_t verilogPreprocParser::CelldefineContext::getRuleIndex() const {
  return verilogPreprocParser::RuleCelldefine;
}

antlrcpp::Any verilogPreprocParser::CelldefineContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitCelldefine(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::CelldefineContext* verilogPreprocParser::celldefine() {
  CelldefineContext *_localctx = _tracker.createInstance<CelldefineContext>(_ctx, getState());
  enterRule(_localctx, 42, verilogPreprocParser::RuleCelldefine);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(275);
    match(verilogPreprocParser::CELLDEFINE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- EndcelldefineContext ------------------------------------------------------------------

verilogPreprocParser::EndcelldefineContext::EndcelldefineContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::EndcelldefineContext::ENDCELLDEFINE() {
  return getToken(verilogPreprocParser::ENDCELLDEFINE, 0);
}


size_t verilogPreprocParser::EndcelldefineContext::getRuleIndex() const {
  return verilogPreprocParser::RuleEndcelldefine;
}

antlrcpp::Any verilogPreprocParser::EndcelldefineContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitEndcelldefine(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::EndcelldefineContext* verilogPreprocParser::endcelldefine() {
  EndcelldefineContext *_localctx = _tracker.createInstance<EndcelldefineContext>(_ctx, getState());
  enterRule(_localctx, 44, verilogPreprocParser::RuleEndcelldefine);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(277);
    match(verilogPreprocParser::ENDCELLDEFINE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Unconnected_driveContext ------------------------------------------------------------------

verilogPreprocParser::Unconnected_driveContext::Unconnected_driveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Unconnected_driveContext::UNCONNECTED_DRIVE() {
  return getToken(verilogPreprocParser::UNCONNECTED_DRIVE, 0);
}


size_t verilogPreprocParser::Unconnected_driveContext::getRuleIndex() const {
  return verilogPreprocParser::RuleUnconnected_drive;
}

antlrcpp::Any verilogPreprocParser::Unconnected_driveContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitUnconnected_drive(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Unconnected_driveContext* verilogPreprocParser::unconnected_drive() {
  Unconnected_driveContext *_localctx = _tracker.createInstance<Unconnected_driveContext>(_ctx, getState());
  enterRule(_localctx, 46, verilogPreprocParser::RuleUnconnected_drive);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(279);
    match(verilogPreprocParser::UNCONNECTED_DRIVE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Nounconnected_driveContext ------------------------------------------------------------------

verilogPreprocParser::Nounconnected_driveContext::Nounconnected_driveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Nounconnected_driveContext::NOUNCONNECTED_DRIVE() {
  return getToken(verilogPreprocParser::NOUNCONNECTED_DRIVE, 0);
}


size_t verilogPreprocParser::Nounconnected_driveContext::getRuleIndex() const {
  return verilogPreprocParser::RuleNounconnected_drive;
}

antlrcpp::Any verilogPreprocParser::Nounconnected_driveContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitNounconnected_drive(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Nounconnected_driveContext* verilogPreprocParser::nounconnected_drive() {
  Nounconnected_driveContext *_localctx = _tracker.createInstance<Nounconnected_driveContext>(_ctx, getState());
  enterRule(_localctx, 48, verilogPreprocParser::RuleNounconnected_drive);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(281);
    match(verilogPreprocParser::NOUNCONNECTED_DRIVE);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Default_nettypeContext ------------------------------------------------------------------

verilogPreprocParser::Default_nettypeContext::Default_nettypeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Default_nettypeContext::DEFAULT_NETTYPE() {
  return getToken(verilogPreprocParser::DEFAULT_NETTYPE, 0);
}

verilogPreprocParser::Default_nettype_valueContext* verilogPreprocParser::Default_nettypeContext::default_nettype_value() {
  return getRuleContext<verilogPreprocParser::Default_nettype_valueContext>(0);
}


size_t verilogPreprocParser::Default_nettypeContext::getRuleIndex() const {
  return verilogPreprocParser::RuleDefault_nettype;
}

antlrcpp::Any verilogPreprocParser::Default_nettypeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitDefault_nettype(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Default_nettypeContext* verilogPreprocParser::default_nettype() {
  Default_nettypeContext *_localctx = _tracker.createInstance<Default_nettypeContext>(_ctx, getState());
  enterRule(_localctx, 50, verilogPreprocParser::RuleDefault_nettype);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(283);
    match(verilogPreprocParser::DEFAULT_NETTYPE);
    setState(284);
    default_nettype_value();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Default_nettype_valueContext ------------------------------------------------------------------

verilogPreprocParser::Default_nettype_valueContext::Default_nettype_valueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Default_nettype_valueContext::WIRE() {
  return getToken(verilogPreprocParser::WIRE, 0);
}

tree::TerminalNode* verilogPreprocParser::Default_nettype_valueContext::TRI() {
  return getToken(verilogPreprocParser::TRI, 0);
}

tree::TerminalNode* verilogPreprocParser::Default_nettype_valueContext::TRI0() {
  return getToken(verilogPreprocParser::TRI0, 0);
}

tree::TerminalNode* verilogPreprocParser::Default_nettype_valueContext::TRI1() {
  return getToken(verilogPreprocParser::TRI1, 0);
}

tree::TerminalNode* verilogPreprocParser::Default_nettype_valueContext::WAND() {
  return getToken(verilogPreprocParser::WAND, 0);
}

tree::TerminalNode* verilogPreprocParser::Default_nettype_valueContext::TRIAND() {
  return getToken(verilogPreprocParser::TRIAND, 0);
}

tree::TerminalNode* verilogPreprocParser::Default_nettype_valueContext::WOR() {
  return getToken(verilogPreprocParser::WOR, 0);
}

tree::TerminalNode* verilogPreprocParser::Default_nettype_valueContext::TRIOR() {
  return getToken(verilogPreprocParser::TRIOR, 0);
}

tree::TerminalNode* verilogPreprocParser::Default_nettype_valueContext::TRIREG() {
  return getToken(verilogPreprocParser::TRIREG, 0);
}

tree::TerminalNode* verilogPreprocParser::Default_nettype_valueContext::UWIRE() {
  return getToken(verilogPreprocParser::UWIRE, 0);
}

tree::TerminalNode* verilogPreprocParser::Default_nettype_valueContext::NONE() {
  return getToken(verilogPreprocParser::NONE, 0);
}


size_t verilogPreprocParser::Default_nettype_valueContext::getRuleIndex() const {
  return verilogPreprocParser::RuleDefault_nettype_value;
}

antlrcpp::Any verilogPreprocParser::Default_nettype_valueContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitDefault_nettype_value(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Default_nettype_valueContext* verilogPreprocParser::default_nettype_value() {
  Default_nettype_valueContext *_localctx = _tracker.createInstance<Default_nettype_valueContext>(_ctx, getState());
  enterRule(_localctx, 52, verilogPreprocParser::RuleDefault_nettype_value);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    setState(299);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 28, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(286);
      match(verilogPreprocParser::WIRE);
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(287);
      match(verilogPreprocParser::TRI);
      break;
    }

    case 3: {
      enterOuterAlt(_localctx, 3);
      setState(288);
      match(verilogPreprocParser::TRI0);
      break;
    }

    case 4: {
      enterOuterAlt(_localctx, 4);
      setState(289);
      match(verilogPreprocParser::TRI1);
      break;
    }

    case 5: {
      enterOuterAlt(_localctx, 5);
      setState(290);
      match(verilogPreprocParser::WAND);
      break;
    }

    case 6: {
      enterOuterAlt(_localctx, 6);
      setState(291);
      match(verilogPreprocParser::TRIAND);
      break;
    }

    case 7: {
      enterOuterAlt(_localctx, 7);
      setState(292);
      match(verilogPreprocParser::WOR);
      break;
    }

    case 8: {
      enterOuterAlt(_localctx, 8);
      setState(293);
      match(verilogPreprocParser::TRIOR);
      break;
    }

    case 9: {
      enterOuterAlt(_localctx, 9);
      setState(294);
      match(verilogPreprocParser::TRIREG);
      break;
    }

    case 10: {
      enterOuterAlt(_localctx, 10);
      setState(295);
      match(verilogPreprocParser::UWIRE);
      break;
    }

    case 11: {
      enterOuterAlt(_localctx, 11);
      setState(296);
      match(verilogPreprocParser::NONE);
      break;
    }

    case 12: {
      enterOuterAlt(_localctx, 12);
      setState(297);

      if (!(language_version >= hdlConvertor::Language::VERILOG2005)) throw FailedPredicateException(this, "language_version >= hdlConvertor::Language::VERILOG2005");
      setState(298);
      match(verilogPreprocParser::UWIRE);
      break;
    }

    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Line_directiveContext ------------------------------------------------------------------

verilogPreprocParser::Line_directiveContext::Line_directiveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Line_directiveContext::LINE() {
  return getToken(verilogPreprocParser::LINE, 0);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::Line_directiveContext::NUM() {
  return getTokens(verilogPreprocParser::NUM);
}

tree::TerminalNode* verilogPreprocParser::Line_directiveContext::NUM(size_t i) {
  return getToken(verilogPreprocParser::NUM, i);
}

tree::TerminalNode* verilogPreprocParser::Line_directiveContext::STR() {
  return getToken(verilogPreprocParser::STR, 0);
}


size_t verilogPreprocParser::Line_directiveContext::getRuleIndex() const {
  return verilogPreprocParser::RuleLine_directive;
}

antlrcpp::Any verilogPreprocParser::Line_directiveContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitLine_directive(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Line_directiveContext* verilogPreprocParser::line_directive() {
  Line_directiveContext *_localctx = _tracker.createInstance<Line_directiveContext>(_ctx, getState());
  enterRule(_localctx, 54, verilogPreprocParser::RuleLine_directive);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(301);
    match(verilogPreprocParser::LINE);
    setState(302);
    match(verilogPreprocParser::NUM);
    setState(303);
    match(verilogPreprocParser::STR);
    setState(304);
    match(verilogPreprocParser::NUM);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Timing_specContext ------------------------------------------------------------------

verilogPreprocParser::Timing_specContext::Timing_specContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Timing_specContext::TIMESCALE() {
  return getToken(verilogPreprocParser::TIMESCALE, 0);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::Timing_specContext::Time_Identifier() {
  return getTokens(verilogPreprocParser::Time_Identifier);
}

tree::TerminalNode* verilogPreprocParser::Timing_specContext::Time_Identifier(size_t i) {
  return getToken(verilogPreprocParser::Time_Identifier, i);
}

tree::TerminalNode* verilogPreprocParser::Timing_specContext::TIMING_SPEC_MODE_SLASH() {
  return getToken(verilogPreprocParser::TIMING_SPEC_MODE_SLASH, 0);
}


size_t verilogPreprocParser::Timing_specContext::getRuleIndex() const {
  return verilogPreprocParser::RuleTiming_spec;
}

antlrcpp::Any verilogPreprocParser::Timing_specContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitTiming_spec(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Timing_specContext* verilogPreprocParser::timing_spec() {
  Timing_specContext *_localctx = _tracker.createInstance<Timing_specContext>(_ctx, getState());
  enterRule(_localctx, 56, verilogPreprocParser::RuleTiming_spec);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(306);
    match(verilogPreprocParser::TIMESCALE);
    setState(307);
    match(verilogPreprocParser::Time_Identifier);
    setState(308);
    match(verilogPreprocParser::TIMING_SPEC_MODE_SLASH);
    setState(309);
    match(verilogPreprocParser::Time_Identifier);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Protected_blockContext ------------------------------------------------------------------

verilogPreprocParser::Protected_blockContext::Protected_blockContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Protected_blockContext::PROTECTED() {
  return getToken(verilogPreprocParser::PROTECTED, 0);
}

tree::TerminalNode* verilogPreprocParser::Protected_blockContext::ENDPROTECTED() {
  return getToken(verilogPreprocParser::ENDPROTECTED, 0);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::Protected_blockContext::PROTECTED_LINE() {
  return getTokens(verilogPreprocParser::PROTECTED_LINE);
}

tree::TerminalNode* verilogPreprocParser::Protected_blockContext::PROTECTED_LINE(size_t i) {
  return getToken(verilogPreprocParser::PROTECTED_LINE, i);
}


size_t verilogPreprocParser::Protected_blockContext::getRuleIndex() const {
  return verilogPreprocParser::RuleProtected_block;
}

antlrcpp::Any verilogPreprocParser::Protected_blockContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitProtected_block(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Protected_blockContext* verilogPreprocParser::protected_block() {
  Protected_blockContext *_localctx = _tracker.createInstance<Protected_blockContext>(_ctx, getState());
  enterRule(_localctx, 58, verilogPreprocParser::RuleProtected_block);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(311);
    match(verilogPreprocParser::PROTECTED);
    setState(315);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == verilogPreprocParser::PROTECTED_LINE) {
      setState(312);
      match(verilogPreprocParser::PROTECTED_LINE);
      setState(317);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(318);
    match(verilogPreprocParser::ENDPROTECTED);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ResetallContext ------------------------------------------------------------------

verilogPreprocParser::ResetallContext::ResetallContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::ResetallContext::RESETALL() {
  return getToken(verilogPreprocParser::RESETALL, 0);
}


size_t verilogPreprocParser::ResetallContext::getRuleIndex() const {
  return verilogPreprocParser::RuleResetall;
}

antlrcpp::Any verilogPreprocParser::ResetallContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitResetall(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::ResetallContext* verilogPreprocParser::resetall() {
  ResetallContext *_localctx = _tracker.createInstance<ResetallContext>(_ctx, getState());
  enterRule(_localctx, 60, verilogPreprocParser::RuleResetall);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(320);
    match(verilogPreprocParser::RESETALL);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- UndefineallContext ------------------------------------------------------------------

verilogPreprocParser::UndefineallContext::UndefineallContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::UndefineallContext::UNDEFINEALL() {
  return getToken(verilogPreprocParser::UNDEFINEALL, 0);
}


size_t verilogPreprocParser::UndefineallContext::getRuleIndex() const {
  return verilogPreprocParser::RuleUndefineall;
}

antlrcpp::Any verilogPreprocParser::UndefineallContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitUndefineall(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::UndefineallContext* verilogPreprocParser::undefineall() {
  UndefineallContext *_localctx = _tracker.createInstance<UndefineallContext>(_ctx, getState());
  enterRule(_localctx, 62, verilogPreprocParser::RuleUndefineall);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(322);
    match(verilogPreprocParser::UNDEFINEALL);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Keywords_directiveContext ------------------------------------------------------------------

verilogPreprocParser::Keywords_directiveContext::Keywords_directiveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Keywords_directiveContext::BEGIN_KEYWORDS() {
  return getToken(verilogPreprocParser::BEGIN_KEYWORDS, 0);
}

verilogPreprocParser::Version_specifierContext* verilogPreprocParser::Keywords_directiveContext::version_specifier() {
  return getRuleContext<verilogPreprocParser::Version_specifierContext>(0);
}


size_t verilogPreprocParser::Keywords_directiveContext::getRuleIndex() const {
  return verilogPreprocParser::RuleKeywords_directive;
}

antlrcpp::Any verilogPreprocParser::Keywords_directiveContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitKeywords_directive(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Keywords_directiveContext* verilogPreprocParser::keywords_directive() {
  Keywords_directiveContext *_localctx = _tracker.createInstance<Keywords_directiveContext>(_ctx, getState());
  enterRule(_localctx, 64, verilogPreprocParser::RuleKeywords_directive);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(324);
    match(verilogPreprocParser::BEGIN_KEYWORDS);
    setState(325);
    version_specifier();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Version_specifierContext ------------------------------------------------------------------

verilogPreprocParser::Version_specifierContext::Version_specifierContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Version_specifierContext::STR() {
  return getToken(verilogPreprocParser::STR, 0);
}


size_t verilogPreprocParser::Version_specifierContext::getRuleIndex() const {
  return verilogPreprocParser::RuleVersion_specifier;
}

antlrcpp::Any verilogPreprocParser::Version_specifierContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitVersion_specifier(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Version_specifierContext* verilogPreprocParser::version_specifier() {
  Version_specifierContext *_localctx = _tracker.createInstance<Version_specifierContext>(_ctx, getState());
  enterRule(_localctx, 66, verilogPreprocParser::RuleVersion_specifier);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(327);
    match(verilogPreprocParser::STR);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Endkeywords_directiveContext ------------------------------------------------------------------

verilogPreprocParser::Endkeywords_directiveContext::Endkeywords_directiveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Endkeywords_directiveContext::END_KEYWORDS() {
  return getToken(verilogPreprocParser::END_KEYWORDS, 0);
}


size_t verilogPreprocParser::Endkeywords_directiveContext::getRuleIndex() const {
  return verilogPreprocParser::RuleEndkeywords_directive;
}

antlrcpp::Any verilogPreprocParser::Endkeywords_directiveContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitEndkeywords_directive(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Endkeywords_directiveContext* verilogPreprocParser::endkeywords_directive() {
  Endkeywords_directiveContext *_localctx = _tracker.createInstance<Endkeywords_directiveContext>(_ctx, getState());
  enterRule(_localctx, 68, verilogPreprocParser::RuleEndkeywords_directive);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(329);
    match(verilogPreprocParser::END_KEYWORDS);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- IncludeContext ------------------------------------------------------------------

verilogPreprocParser::IncludeContext::IncludeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::IncludeContext::INCLUDE() {
  return getToken(verilogPreprocParser::INCLUDE, 0);
}

tree::TerminalNode* verilogPreprocParser::IncludeContext::STR() {
  return getToken(verilogPreprocParser::STR, 0);
}

verilogPreprocParser::Macro_callContext* verilogPreprocParser::IncludeContext::macro_call() {
  return getRuleContext<verilogPreprocParser::Macro_callContext>(0);
}


size_t verilogPreprocParser::IncludeContext::getRuleIndex() const {
  return verilogPreprocParser::RuleInclude;
}

antlrcpp::Any verilogPreprocParser::IncludeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitInclude(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::IncludeContext* verilogPreprocParser::include() {
  IncludeContext *_localctx = _tracker.createInstance<IncludeContext>(_ctx, getState());
  enterRule(_localctx, 70, verilogPreprocParser::RuleInclude);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(331);
    match(verilogPreprocParser::INCLUDE);
    setState(335);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 30, _ctx)) {
    case 1: {
      setState(332);
      match(verilogPreprocParser::STR);
      break;
    }

    case 2: {
      setState(333);

      if (!(language_version >= hdlConvertor::Language::SV2005)) throw FailedPredicateException(this, "language_version >= hdlConvertor::Language::SV2005");
      setState(334);
      macro_call();
      break;
    }

    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PragmaContext ------------------------------------------------------------------

verilogPreprocParser::PragmaContext::PragmaContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::PragmaContext::PRAGMA() {
  return getToken(verilogPreprocParser::PRAGMA, 0);
}

verilogPreprocParser::Pragma_nameContext* verilogPreprocParser::PragmaContext::pragma_name() {
  return getRuleContext<verilogPreprocParser::Pragma_nameContext>(0);
}

tree::TerminalNode* verilogPreprocParser::PragmaContext::NEW_LINE() {
  return getToken(verilogPreprocParser::NEW_LINE, 0);
}

tree::TerminalNode* verilogPreprocParser::PragmaContext::EOF() {
  return getToken(verilogPreprocParser::EOF, 0);
}

std::vector<verilogPreprocParser::Pragma_expressionContext *> verilogPreprocParser::PragmaContext::pragma_expression() {
  return getRuleContexts<verilogPreprocParser::Pragma_expressionContext>();
}

verilogPreprocParser::Pragma_expressionContext* verilogPreprocParser::PragmaContext::pragma_expression(size_t i) {
  return getRuleContext<verilogPreprocParser::Pragma_expressionContext>(i);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::PragmaContext::COMMA() {
  return getTokens(verilogPreprocParser::COMMA);
}

tree::TerminalNode* verilogPreprocParser::PragmaContext::COMMA(size_t i) {
  return getToken(verilogPreprocParser::COMMA, i);
}


size_t verilogPreprocParser::PragmaContext::getRuleIndex() const {
  return verilogPreprocParser::RulePragma;
}

antlrcpp::Any verilogPreprocParser::PragmaContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitPragma(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::PragmaContext* verilogPreprocParser::pragma() {
  PragmaContext *_localctx = _tracker.createInstance<PragmaContext>(_ctx, getState());
  enterRule(_localctx, 72, verilogPreprocParser::RulePragma);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(337);
    match(verilogPreprocParser::PRAGMA);
    setState(338);
    pragma_name();
    setState(347);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & ((1ULL << verilogPreprocParser::STR)
      | (1ULL << verilogPreprocParser::LP)
      | (1ULL << verilogPreprocParser::ID)
      | (1ULL << verilogPreprocParser::NUM))) != 0)) {
      setState(339);
      pragma_expression();
      setState(344);
      _errHandler->sync(this);
      _la = _input->LA(1);
      while (_la == verilogPreprocParser::COMMA) {
        setState(340);
        match(verilogPreprocParser::COMMA);
        setState(341);
        pragma_expression();
        setState(346);
        _errHandler->sync(this);
        _la = _input->LA(1);
      }
    }
    setState(349);
    _la = _input->LA(1);
    if (!(_la == verilogPreprocParser::EOF

    || _la == verilogPreprocParser::NEW_LINE)) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Pragma_nameContext ------------------------------------------------------------------

verilogPreprocParser::Pragma_nameContext::Pragma_nameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Pragma_nameContext::ID() {
  return getToken(verilogPreprocParser::ID, 0);
}


size_t verilogPreprocParser::Pragma_nameContext::getRuleIndex() const {
  return verilogPreprocParser::RulePragma_name;
}

antlrcpp::Any verilogPreprocParser::Pragma_nameContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitPragma_name(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Pragma_nameContext* verilogPreprocParser::pragma_name() {
  Pragma_nameContext *_localctx = _tracker.createInstance<Pragma_nameContext>(_ctx, getState());
  enterRule(_localctx, 74, verilogPreprocParser::RulePragma_name);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(351);
    match(verilogPreprocParser::ID);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Pragma_expressionContext ------------------------------------------------------------------

verilogPreprocParser::Pragma_expressionContext::Pragma_expressionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

verilogPreprocParser::Pragma_keywordContext* verilogPreprocParser::Pragma_expressionContext::pragma_keyword() {
  return getRuleContext<verilogPreprocParser::Pragma_keywordContext>(0);
}

tree::TerminalNode* verilogPreprocParser::Pragma_expressionContext::EQUAL() {
  return getToken(verilogPreprocParser::EQUAL, 0);
}

verilogPreprocParser::Pragma_valueContext* verilogPreprocParser::Pragma_expressionContext::pragma_value() {
  return getRuleContext<verilogPreprocParser::Pragma_valueContext>(0);
}


size_t verilogPreprocParser::Pragma_expressionContext::getRuleIndex() const {
  return verilogPreprocParser::RulePragma_expression;
}

antlrcpp::Any verilogPreprocParser::Pragma_expressionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitPragma_expression(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Pragma_expressionContext* verilogPreprocParser::pragma_expression() {
  Pragma_expressionContext *_localctx = _tracker.createInstance<Pragma_expressionContext>(_ctx, getState());
  enterRule(_localctx, 76, verilogPreprocParser::RulePragma_expression);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    setState(359);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 33, _ctx)) {
    case 1: {
      enterOuterAlt(_localctx, 1);
      setState(353);
      pragma_keyword();
      break;
    }

    case 2: {
      enterOuterAlt(_localctx, 2);
      setState(354);
      pragma_keyword();
      setState(355);
      match(verilogPreprocParser::EQUAL);
      setState(356);
      pragma_value();
      break;
    }

    case 3: {
      enterOuterAlt(_localctx, 3);
      setState(358);
      pragma_value();
      break;
    }

    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Pragma_valueContext ------------------------------------------------------------------

verilogPreprocParser::Pragma_valueContext::Pragma_valueContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Pragma_valueContext::LP() {
  return getToken(verilogPreprocParser::LP, 0);
}

std::vector<verilogPreprocParser::Pragma_expressionContext *> verilogPreprocParser::Pragma_valueContext::pragma_expression() {
  return getRuleContexts<verilogPreprocParser::Pragma_expressionContext>();
}

verilogPreprocParser::Pragma_expressionContext* verilogPreprocParser::Pragma_valueContext::pragma_expression(size_t i) {
  return getRuleContext<verilogPreprocParser::Pragma_expressionContext>(i);
}

tree::TerminalNode* verilogPreprocParser::Pragma_valueContext::RP() {
  return getToken(verilogPreprocParser::RP, 0);
}

std::vector<tree::TerminalNode *> verilogPreprocParser::Pragma_valueContext::COMMA() {
  return getTokens(verilogPreprocParser::COMMA);
}

tree::TerminalNode* verilogPreprocParser::Pragma_valueContext::COMMA(size_t i) {
  return getToken(verilogPreprocParser::COMMA, i);
}

tree::TerminalNode* verilogPreprocParser::Pragma_valueContext::NUM() {
  return getToken(verilogPreprocParser::NUM, 0);
}

tree::TerminalNode* verilogPreprocParser::Pragma_valueContext::STR() {
  return getToken(verilogPreprocParser::STR, 0);
}

tree::TerminalNode* verilogPreprocParser::Pragma_valueContext::ID() {
  return getToken(verilogPreprocParser::ID, 0);
}


size_t verilogPreprocParser::Pragma_valueContext::getRuleIndex() const {
  return verilogPreprocParser::RulePragma_value;
}

antlrcpp::Any verilogPreprocParser::Pragma_valueContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitPragma_value(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Pragma_valueContext* verilogPreprocParser::pragma_value() {
  Pragma_valueContext *_localctx = _tracker.createInstance<Pragma_valueContext>(_ctx, getState());
  enterRule(_localctx, 78, verilogPreprocParser::RulePragma_value);
  size_t _la = 0;

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    setState(375);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case verilogPreprocParser::LP: {
        enterOuterAlt(_localctx, 1);
        setState(361);
        match(verilogPreprocParser::LP);
        setState(362);
        pragma_expression();
        setState(367);
        _errHandler->sync(this);
        _la = _input->LA(1);
        while (_la == verilogPreprocParser::COMMA) {
          setState(363);
          match(verilogPreprocParser::COMMA);
          setState(364);
          pragma_expression();
          setState(369);
          _errHandler->sync(this);
          _la = _input->LA(1);
        }
        setState(370);
        match(verilogPreprocParser::RP);
        break;
      }

      case verilogPreprocParser::NUM: {
        enterOuterAlt(_localctx, 2);
        setState(372);
        match(verilogPreprocParser::NUM);
        break;
      }

      case verilogPreprocParser::STR: {
        enterOuterAlt(_localctx, 3);
        setState(373);
        match(verilogPreprocParser::STR);
        break;
      }

      case verilogPreprocParser::ID: {
        enterOuterAlt(_localctx, 4);
        setState(374);
        match(verilogPreprocParser::ID);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- Pragma_keywordContext ------------------------------------------------------------------

verilogPreprocParser::Pragma_keywordContext::Pragma_keywordContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* verilogPreprocParser::Pragma_keywordContext::ID() {
  return getToken(verilogPreprocParser::ID, 0);
}


size_t verilogPreprocParser::Pragma_keywordContext::getRuleIndex() const {
  return verilogPreprocParser::RulePragma_keyword;
}

antlrcpp::Any verilogPreprocParser::Pragma_keywordContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<verilogPreprocParserVisitor*>(visitor))
    return parserVisitor->visitPragma_keyword(this);
  else
    return visitor->visitChildren(this);
}

verilogPreprocParser::Pragma_keywordContext* verilogPreprocParser::pragma_keyword() {
  Pragma_keywordContext *_localctx = _tracker.createInstance<Pragma_keywordContext>(_ctx, getState());
  enterRule(_localctx, 80, verilogPreprocParser::RulePragma_keyword);

  auto onExit = finally([=] {
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(377);
    match(verilogPreprocParser::ID);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

bool verilogPreprocParser::sempred(RuleContext *context, size_t ruleIndex, size_t predicateIndex) {
  switch (ruleIndex) {
    case 2: return preprocess_directiveSempred(dynamic_cast<Preprocess_directiveContext *>(context), predicateIndex);
    case 4: return define_argsSempred(dynamic_cast<Define_argsContext *>(context), predicateIndex);
    case 26: return default_nettype_valueSempred(dynamic_cast<Default_nettype_valueContext *>(context), predicateIndex);
    case 35: return includeSempred(dynamic_cast<IncludeContext *>(context), predicateIndex);

  default:
    break;
  }
  return true;
}

bool verilogPreprocParser::preprocess_directiveSempred(Preprocess_directiveContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 0: return language_version >= hdlConvertor::Language::SV2009;
    case 1: return language_version >= hdlConvertor::Language::VERILOG2005;

  default:
    break;
  }
  return true;
}

bool verilogPreprocParser::define_argsSempred(Define_argsContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 2: return  language_version >= hdlConvertor::Language::SV2009 ;
    case 3: return  language_version < hdlConvertor::Language::SV2009 ;

  default:
    break;
  }
  return true;
}

bool verilogPreprocParser::default_nettype_valueSempred(Default_nettype_valueContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 4: return language_version >= hdlConvertor::Language::VERILOG2005;

  default:
    break;
  }
  return true;
}

bool verilogPreprocParser::includeSempred(IncludeContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 5: return language_version >= hdlConvertor::Language::SV2005;

  default:
    break;
  }
  return true;
}

// Static vars and initialization.
std::vector<dfa::DFA> verilogPreprocParser::_decisionToDFA;
atn::PredictionContextCache verilogPreprocParser::_sharedContextCache;

// We own the ATN which in turn owns the ATN states.
atn::ATN verilogPreprocParser::_atn;
std::vector<uint16_t> verilogPreprocParser::_serializedATN;

std::vector<std::string> verilogPreprocParser::_ruleNames = {
  "file", "text", "preprocess_directive", "define", "define_args", "define_args_with_def_val", 
  "param_with_def_val", "define_args_basic", "replacement", "default_text", 
  "conditional", "ifdef_directive", "ifndef_directive", "else_group_of_lines", 
  "group_of_lines", "macro_call", "value", "macro_id", "var_id", "cond_id", 
  "undef", "celldefine", "endcelldefine", "unconnected_drive", "nounconnected_drive", 
  "default_nettype", "default_nettype_value", "line_directive", "timing_spec", 
  "protected_block", "resetall", "undefineall", "keywords_directive", "version_specifier", 
  "endkeywords_directive", "include", "pragma", "pragma_name", "pragma_expression", 
  "pragma_value", "pragma_keyword"
};

std::vector<std::string> verilogPreprocParser::_literalNames = {
  "", "", "", "", "", "'`'", "", "", "", "", "", "", "", "", "", "", "", 
  "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", 
  "", "", "", "", "", "", "", "", "", "", "", "'wire'", "'tri'", "'tri0'", 
  "'tri1'", "'wand'", "'triand'", "'wor'", "'trior'", "'trireg'", "'uwire'", 
  "'none'", "", "", "'/'", "", "", "", "", "", "'`endprotected'", "", "'='"
};

std::vector<std::string> verilogPreprocParser::_symbolicNames = {
  "", "STR", "LINE_COMMENT", "COMMENT", "CODE", "MACRO_ENTER", "INCLUDE", 
  "DEFINE", "IFNDEF", "IFDEF", "ELSIF", "ELSE", "ENDIF", "UNDEF", "BEGIN_KEYWORDS", 
  "END_KEYWORDS", "PRAGMA", "UNDEFINEALL", "RESETALL", "CELLDEFINE", "ENDCELLDEFINE", 
  "TIMESCALE", "DEFAULT_NETTYPE", "LINE", "UNCONNECTED_DRIVE", "NOUNCONNECTED_DRIVE", 
  "PROTECTED", "OTHER_MACRO_CALL_WITH_ARGS", "OTHER_MACRO_CALL_NO_ARGS", 
  "DM_LINE_COMMENT", "DM_COMMENT", "LINE_ESCAPE", "LP", "RP", "COMMA", "EQUAL", 
  "DM_NEW_LINE", "WS", "ID", "EXPR_MODE_RP", "EXPR_MODE_COMMA", "DB_LINE_ESCAPE", 
  "NEW_LINE", "MA_COMMA", "MA_RP", "NUM", "WIRE", "TRI", "TRI0", "TRI1", 
  "WAND", "TRIAND", "WOR", "TRIOR", "TRIREG", "UWIRE", "NONE", "LINE_MODE_WS", 
  "Time_Identifier", "TIMING_SPEC_MODE_SLASH", "TIMING_SPEC_MODE_WS", "INCLUDE_MODE_MACRO_ENTER", 
  "INCLUDE_MODE_WS", "PRAGMA_WS", "PROTECTED_WS", "ENDPROTECTED", "PROTECTED_LINE", 
  "PRAGMA_EQUAL"
};

dfa::Vocabulary verilogPreprocParser::_vocabulary(_literalNames, _symbolicNames);

std::vector<std::string> verilogPreprocParser::_tokenNames;

verilogPreprocParser::Initializer::Initializer() {
	for (size_t i = 0; i < _symbolicNames.size(); ++i) {
		std::string name = _vocabulary.getLiteralName(i);
		if (name.empty()) {
			name = _vocabulary.getSymbolicName(i);
		}

		if (name.empty()) {
			_tokenNames.push_back("<INVALID>");
		} else {
      _tokenNames.push_back(name);
    }
	}

  _serializedATN = {
    0x3, 0x608b, 0xa72a, 0x8133, 0xb9ed, 0x417c, 0x3be7, 0x7786, 0x5964, 
    0x3, 0x45, 0x17e, 0x4, 0x2, 0x9, 0x2, 0x4, 0x3, 0x9, 0x3, 0x4, 0x4, 
    0x9, 0x4, 0x4, 0x5, 0x9, 0x5, 0x4, 0x6, 0x9, 0x6, 0x4, 0x7, 0x9, 0x7, 
    0x4, 0x8, 0x9, 0x8, 0x4, 0x9, 0x9, 0x9, 0x4, 0xa, 0x9, 0xa, 0x4, 0xb, 
    0x9, 0xb, 0x4, 0xc, 0x9, 0xc, 0x4, 0xd, 0x9, 0xd, 0x4, 0xe, 0x9, 0xe, 
    0x4, 0xf, 0x9, 0xf, 0x4, 0x10, 0x9, 0x10, 0x4, 0x11, 0x9, 0x11, 0x4, 
    0x12, 0x9, 0x12, 0x4, 0x13, 0x9, 0x13, 0x4, 0x14, 0x9, 0x14, 0x4, 0x15, 
    0x9, 0x15, 0x4, 0x16, 0x9, 0x16, 0x4, 0x17, 0x9, 0x17, 0x4, 0x18, 0x9, 
    0x18, 0x4, 0x19, 0x9, 0x19, 0x4, 0x1a, 0x9, 0x1a, 0x4, 0x1b, 0x9, 0x1b, 
    0x4, 0x1c, 0x9, 0x1c, 0x4, 0x1d, 0x9, 0x1d, 0x4, 0x1e, 0x9, 0x1e, 0x4, 
    0x1f, 0x9, 0x1f, 0x4, 0x20, 0x9, 0x20, 0x4, 0x21, 0x9, 0x21, 0x4, 0x22, 
    0x9, 0x22, 0x4, 0x23, 0x9, 0x23, 0x4, 0x24, 0x9, 0x24, 0x4, 0x25, 0x9, 
    0x25, 0x4, 0x26, 0x9, 0x26, 0x4, 0x27, 0x9, 0x27, 0x4, 0x28, 0x9, 0x28, 
    0x4, 0x29, 0x9, 0x29, 0x4, 0x2a, 0x9, 0x2a, 0x3, 0x2, 0x7, 0x2, 0x56, 
    0xa, 0x2, 0xc, 0x2, 0xe, 0x2, 0x59, 0xb, 0x2, 0x3, 0x2, 0x3, 0x2, 0x3, 
    0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 
    0x3, 0x3, 0x3, 0x5, 0x3, 0x66, 0xa, 0x3, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 
    0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 
    0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 
    0x3, 0x4, 0x3, 0x4, 0x3, 0x4, 0x5, 0x4, 0x7c, 0xa, 0x4, 0x5, 0x4, 0x7e, 
    0xa, 0x4, 0x3, 0x5, 0x3, 0x5, 0x3, 0x5, 0x3, 0x5, 0x5, 0x5, 0x84, 0xa, 
    0x5, 0x3, 0x5, 0x5, 0x5, 0x87, 0xa, 0x5, 0x3, 0x5, 0x7, 0x5, 0x8a, 0xa, 
    0x5, 0xc, 0x5, 0xe, 0x5, 0x8d, 0xb, 0x5, 0x3, 0x5, 0x5, 0x5, 0x90, 0xa, 
    0x5, 0x3, 0x5, 0x3, 0x5, 0x3, 0x6, 0x3, 0x6, 0x3, 0x6, 0x3, 0x6, 0x5, 
    0x6, 0x98, 0xa, 0x6, 0x3, 0x7, 0x3, 0x7, 0x3, 0x7, 0x7, 0x7, 0x9d, 0xa, 
    0x7, 0xc, 0x7, 0xe, 0x7, 0xa0, 0xb, 0x7, 0x3, 0x8, 0x3, 0x8, 0x3, 0x8, 
    0x5, 0x8, 0xa5, 0xa, 0x8, 0x5, 0x8, 0xa7, 0xa, 0x8, 0x3, 0x9, 0x3, 0x9, 
    0x3, 0x9, 0x7, 0x9, 0xac, 0xa, 0x9, 0xc, 0x9, 0xe, 0x9, 0xaf, 0xb, 0x9, 
    0x3, 0xa, 0x6, 0xa, 0xb2, 0xa, 0xa, 0xd, 0xa, 0xe, 0xa, 0xb3, 0x3, 0xb, 
    0x6, 0xb, 0xb7, 0xa, 0xb, 0xd, 0xb, 0xe, 0xb, 0xb8, 0x3, 0xc, 0x3, 0xc, 
    0x5, 0xc, 0xbd, 0xa, 0xc, 0x3, 0xd, 0x3, 0xd, 0x3, 0xd, 0x3, 0xd, 0x3, 
    0xd, 0x3, 0xd, 0x3, 0xd, 0x7, 0xd, 0xc6, 0xa, 0xd, 0xc, 0xd, 0xe, 0xd, 
    0xc9, 0xb, 0xd, 0x3, 0xd, 0x3, 0xd, 0x5, 0xd, 0xcd, 0xa, 0xd, 0x3, 0xd, 
    0x3, 0xd, 0x3, 0xe, 0x3, 0xe, 0x3, 0xe, 0x3, 0xe, 0x3, 0xe, 0x3, 0xe, 
    0x3, 0xe, 0x7, 0xe, 0xd8, 0xa, 0xe, 0xc, 0xe, 0xe, 0xe, 0xdb, 0xb, 0xe, 
    0x3, 0xe, 0x3, 0xe, 0x5, 0xe, 0xdf, 0xa, 0xe, 0x3, 0xe, 0x3, 0xe, 0x3, 
    0xf, 0x3, 0xf, 0x3, 0x10, 0x7, 0x10, 0xe6, 0xa, 0x10, 0xc, 0x10, 0xe, 
    0x10, 0xe9, 0xb, 0x10, 0x3, 0x11, 0x3, 0x11, 0x3, 0x11, 0x5, 0x11, 0xee, 
    0xa, 0x11, 0x3, 0x11, 0x3, 0x11, 0x5, 0x11, 0xf2, 0xa, 0x11, 0x7, 0x11, 
    0xf4, 0xa, 0x11, 0xc, 0x11, 0xe, 0x11, 0xf7, 0xb, 0x11, 0x3, 0x11, 0x5, 
    0x11, 0xfa, 0xa, 0x11, 0x3, 0x12, 0x6, 0x12, 0xfd, 0xa, 0x12, 0xd, 0x12, 
    0xe, 0x12, 0xfe, 0x3, 0x13, 0x3, 0x13, 0x3, 0x14, 0x7, 0x14, 0x104, 
    0xa, 0x14, 0xc, 0x14, 0xe, 0x14, 0x107, 0xb, 0x14, 0x3, 0x14, 0x3, 0x14, 
    0x7, 0x14, 0x10b, 0xa, 0x14, 0xc, 0x14, 0xe, 0x14, 0x10e, 0xb, 0x14, 
    0x3, 0x15, 0x3, 0x15, 0x3, 0x16, 0x3, 0x16, 0x3, 0x16, 0x3, 0x16, 0x3, 
    0x17, 0x3, 0x17, 0x3, 0x18, 0x3, 0x18, 0x3, 0x19, 0x3, 0x19, 0x3, 0x1a, 
    0x3, 0x1a, 0x3, 0x1b, 0x3, 0x1b, 0x3, 0x1b, 0x3, 0x1c, 0x3, 0x1c, 0x3, 
    0x1c, 0x3, 0x1c, 0x3, 0x1c, 0x3, 0x1c, 0x3, 0x1c, 0x3, 0x1c, 0x3, 0x1c, 
    0x3, 0x1c, 0x3, 0x1c, 0x3, 0x1c, 0x3, 0x1c, 0x5, 0x1c, 0x12e, 0xa, 0x1c, 
    0x3, 0x1d, 0x3, 0x1d, 0x3, 0x1d, 0x3, 0x1d, 0x3, 0x1d, 0x3, 0x1e, 0x3, 
    0x1e, 0x3, 0x1e, 0x3, 0x1e, 0x3, 0x1e, 0x3, 0x1f, 0x3, 0x1f, 0x7, 0x1f, 
    0x13c, 0xa, 0x1f, 0xc, 0x1f, 0xe, 0x1f, 0x13f, 0xb, 0x1f, 0x3, 0x1f, 
    0x3, 0x1f, 0x3, 0x20, 0x3, 0x20, 0x3, 0x21, 0x3, 0x21, 0x3, 0x22, 0x3, 
    0x22, 0x3, 0x22, 0x3, 0x23, 0x3, 0x23, 0x3, 0x24, 0x3, 0x24, 0x3, 0x25, 
    0x3, 0x25, 0x3, 0x25, 0x3, 0x25, 0x5, 0x25, 0x152, 0xa, 0x25, 0x3, 0x26, 
    0x3, 0x26, 0x3, 0x26, 0x3, 0x26, 0x3, 0x26, 0x7, 0x26, 0x159, 0xa, 0x26, 
    0xc, 0x26, 0xe, 0x26, 0x15c, 0xb, 0x26, 0x5, 0x26, 0x15e, 0xa, 0x26, 
    0x3, 0x26, 0x3, 0x26, 0x3, 0x27, 0x3, 0x27, 0x3, 0x28, 0x3, 0x28, 0x3, 
    0x28, 0x3, 0x28, 0x3, 0x28, 0x3, 0x28, 0x5, 0x28, 0x16a, 0xa, 0x28, 
    0x3, 0x29, 0x3, 0x29, 0x3, 0x29, 0x3, 0x29, 0x7, 0x29, 0x170, 0xa, 0x29, 
    0xc, 0x29, 0xe, 0x29, 0x173, 0xb, 0x29, 0x3, 0x29, 0x3, 0x29, 0x3, 0x29, 
    0x3, 0x29, 0x3, 0x29, 0x5, 0x29, 0x17a, 0xa, 0x29, 0x3, 0x2a, 0x3, 0x2a, 
    0x3, 0x2a, 0x2, 0x2, 0x2b, 0x2, 0x4, 0x6, 0x8, 0xa, 0xc, 0xe, 0x10, 
    0x12, 0x14, 0x16, 0x18, 0x1a, 0x1c, 0x1e, 0x20, 0x22, 0x24, 0x26, 0x28, 
    0x2a, 0x2c, 0x2e, 0x30, 0x32, 0x34, 0x36, 0x38, 0x3a, 0x3c, 0x3e, 0x40, 
    0x42, 0x44, 0x46, 0x48, 0x4a, 0x4c, 0x4e, 0x50, 0x52, 0x2, 0x5, 0x4, 
    0x3, 0x4, 0x4, 0x2c, 0x2c, 0x4, 0x3, 0x27, 0x27, 0x2c, 0x2c, 0x3, 0x3, 
    0x2c, 0x2c, 0x2, 0x19b, 0x2, 0x57, 0x3, 0x2, 0x2, 0x2, 0x4, 0x65, 0x3, 
    0x2, 0x2, 0x2, 0x6, 0x7d, 0x3, 0x2, 0x2, 0x2, 0x8, 0x7f, 0x3, 0x2, 0x2, 
    0x2, 0xa, 0x97, 0x3, 0x2, 0x2, 0x2, 0xc, 0x99, 0x3, 0x2, 0x2, 0x2, 0xe, 
    0xa1, 0x3, 0x2, 0x2, 0x2, 0x10, 0xa8, 0x3, 0x2, 0x2, 0x2, 0x12, 0xb1, 
    0x3, 0x2, 0x2, 0x2, 0x14, 0xb6, 0x3, 0x2, 0x2, 0x2, 0x16, 0xbc, 0x3, 
    0x2, 0x2, 0x2, 0x18, 0xbe, 0x3, 0x2, 0x2, 0x2, 0x1a, 0xd0, 0x3, 0x2, 
    0x2, 0x2, 0x1c, 0xe2, 0x3, 0x2, 0x2, 0x2, 0x1e, 0xe7, 0x3, 0x2, 0x2, 
    0x2, 0x20, 0xf9, 0x3, 0x2, 0x2, 0x2, 0x22, 0xfc, 0x3, 0x2, 0x2, 0x2, 
    0x24, 0x100, 0x3, 0x2, 0x2, 0x2, 0x26, 0x105, 0x3, 0x2, 0x2, 0x2, 0x28, 
    0x10f, 0x3, 0x2, 0x2, 0x2, 0x2a, 0x111, 0x3, 0x2, 0x2, 0x2, 0x2c, 0x115, 
    0x3, 0x2, 0x2, 0x2, 0x2e, 0x117, 0x3, 0x2, 0x2, 0x2, 0x30, 0x119, 0x3, 
    0x2, 0x2, 0x2, 0x32, 0x11b, 0x3, 0x2, 0x2, 0x2, 0x34, 0x11d, 0x3, 0x2, 
    0x2, 0x2, 0x36, 0x12d, 0x3, 0x2, 0x2, 0x2, 0x38, 0x12f, 0x3, 0x2, 0x2, 
    0x2, 0x3a, 0x134, 0x3, 0x2, 0x2, 0x2, 0x3c, 0x139, 0x3, 0x2, 0x2, 0x2, 
    0x3e, 0x142, 0x3, 0x2, 0x2, 0x2, 0x40, 0x144, 0x3, 0x2, 0x2, 0x2, 0x42, 
    0x146, 0x3, 0x2, 0x2, 0x2, 0x44, 0x149, 0x3, 0x2, 0x2, 0x2, 0x46, 0x14b, 
    0x3, 0x2, 0x2, 0x2, 0x48, 0x14d, 0x3, 0x2, 0x2, 0x2, 0x4a, 0x153, 0x3, 
    0x2, 0x2, 0x2, 0x4c, 0x161, 0x3, 0x2, 0x2, 0x2, 0x4e, 0x169, 0x3, 0x2, 
    0x2, 0x2, 0x50, 0x179, 0x3, 0x2, 0x2, 0x2, 0x52, 0x17b, 0x3, 0x2, 0x2, 
    0x2, 0x54, 0x56, 0x5, 0x4, 0x3, 0x2, 0x55, 0x54, 0x3, 0x2, 0x2, 0x2, 
    0x56, 0x59, 0x3, 0x2, 0x2, 0x2, 0x57, 0x55, 0x3, 0x2, 0x2, 0x2, 0x57, 
    0x58, 0x3, 0x2, 0x2, 0x2, 0x58, 0x5a, 0x3, 0x2, 0x2, 0x2, 0x59, 0x57, 
    0x3, 0x2, 0x2, 0x2, 0x5a, 0x5b, 0x7, 0x2, 0x2, 0x3, 0x5b, 0x3, 0x3, 
    0x2, 0x2, 0x2, 0x5c, 0x66, 0x5, 0x6, 0x4, 0x2, 0x5d, 0x66, 0x7, 0x4, 
    0x2, 0x2, 0x5e, 0x66, 0x7, 0x6, 0x2, 0x2, 0x5f, 0x66, 0x7, 0x2c, 0x2, 
    0x2, 0x60, 0x66, 0x7, 0x2f, 0x2, 0x2, 0x61, 0x66, 0x7, 0x28, 0x2, 0x2, 
    0x62, 0x66, 0x7, 0x3, 0x2, 0x2, 0x63, 0x66, 0x7, 0x2c, 0x2, 0x2, 0x64, 
    0x66, 0x7, 0x5, 0x2, 0x2, 0x65, 0x5c, 0x3, 0x2, 0x2, 0x2, 0x65, 0x5d, 
    0x3, 0x2, 0x2, 0x2, 0x65, 0x5e, 0x3, 0x2, 0x2, 0x2, 0x65, 0x5f, 0x3, 
    0x2, 0x2, 0x2, 0x65, 0x60, 0x3, 0x2, 0x2, 0x2, 0x65, 0x61, 0x3, 0x2, 
    0x2, 0x2, 0x65, 0x62, 0x3, 0x2, 0x2, 0x2, 0x65, 0x63, 0x3, 0x2, 0x2, 
    0x2, 0x65, 0x64, 0x3, 0x2, 0x2, 0x2, 0x66, 0x5, 0x3, 0x2, 0x2, 0x2, 
    0x67, 0x7e, 0x5, 0x8, 0x5, 0x2, 0x68, 0x7e, 0x5, 0x16, 0xc, 0x2, 0x69, 
    0x7e, 0x5, 0x20, 0x11, 0x2, 0x6a, 0x7e, 0x5, 0x3e, 0x20, 0x2, 0x6b, 
    0x7e, 0x5, 0x2a, 0x16, 0x2, 0x6c, 0x7e, 0x5, 0x48, 0x25, 0x2, 0x6d, 
    0x7e, 0x5, 0x2c, 0x17, 0x2, 0x6e, 0x7e, 0x5, 0x2e, 0x18, 0x2, 0x6f, 
    0x7e, 0x5, 0x30, 0x19, 0x2, 0x70, 0x7e, 0x5, 0x32, 0x1a, 0x2, 0x71, 
    0x7e, 0x5, 0x34, 0x1b, 0x2, 0x72, 0x7e, 0x5, 0x38, 0x1d, 0x2, 0x73, 
    0x7e, 0x5, 0x3a, 0x1e, 0x2, 0x74, 0x7e, 0x5, 0x3c, 0x1f, 0x2, 0x75, 
    0x76, 0x6, 0x4, 0x2, 0x2, 0x76, 0x7e, 0x5, 0x40, 0x21, 0x2, 0x77, 0x7b, 
    0x6, 0x4, 0x3, 0x2, 0x78, 0x7c, 0x5, 0x42, 0x22, 0x2, 0x79, 0x7c, 0x5, 
    0x46, 0x24, 0x2, 0x7a, 0x7c, 0x5, 0x4a, 0x26, 0x2, 0x7b, 0x78, 0x3, 
    0x2, 0x2, 0x2, 0x7b, 0x79, 0x3, 0x2, 0x2, 0x2, 0x7b, 0x7a, 0x3, 0x2, 
    0x2, 0x2, 0x7c, 0x7e, 0x3, 0x2, 0x2, 0x2, 0x7d, 0x67, 0x3, 0x2, 0x2, 
    0x2, 0x7d, 0x68, 0x3, 0x2, 0x2, 0x2, 0x7d, 0x69, 0x3, 0x2, 0x2, 0x2, 
    0x7d, 0x6a, 0x3, 0x2, 0x2, 0x2, 0x7d, 0x6b, 0x3, 0x2, 0x2, 0x2, 0x7d, 
    0x6c, 0x3, 0x2, 0x2, 0x2, 0x7d, 0x6d, 0x3, 0x2, 0x2, 0x2, 0x7d, 0x6e, 
    0x3, 0x2, 0x2, 0x2, 0x7d, 0x6f, 0x3, 0x2, 0x2, 0x2, 0x7d, 0x70, 0x3, 
    0x2, 0x2, 0x2, 0x7d, 0x71, 0x3, 0x2, 0x2, 0x2, 0x7d, 0x72, 0x3, 0x2, 
    0x2, 0x2, 0x7d, 0x73, 0x3, 0x2, 0x2, 0x2, 0x7d, 0x74, 0x3, 0x2, 0x2, 
    0x2, 0x7d, 0x75, 0x3, 0x2, 0x2, 0x2, 0x7d, 0x77, 0x3, 0x2, 0x2, 0x2, 
    0x7e, 0x7, 0x3, 0x2, 0x2, 0x2, 0x7f, 0x80, 0x7, 0x9, 0x2, 0x2, 0x80, 
    0x86, 0x5, 0x24, 0x13, 0x2, 0x81, 0x83, 0x7, 0x22, 0x2, 0x2, 0x82, 0x84, 
    0x5, 0xa, 0x6, 0x2, 0x83, 0x82, 0x3, 0x2, 0x2, 0x2, 0x83, 0x84, 0x3, 
    0x2, 0x2, 0x2, 0x84, 0x85, 0x3, 0x2, 0x2, 0x2, 0x85, 0x87, 0x7, 0x23, 
    0x2, 0x2, 0x86, 0x81, 0x3, 0x2, 0x2, 0x2, 0x86, 0x87, 0x3, 0x2, 0x2, 
    0x2, 0x87, 0x8b, 0x3, 0x2, 0x2, 0x2, 0x88, 0x8a, 0x7, 0x27, 0x2, 0x2, 
    0x89, 0x88, 0x3, 0x2, 0x2, 0x2, 0x8a, 0x8d, 0x3, 0x2, 0x2, 0x2, 0x8b, 
    0x89, 0x3, 0x2, 0x2, 0x2, 0x8b, 0x8c, 0x3, 0x2, 0x2, 0x2, 0x8c, 0x8f, 
    0x3, 0x2, 0x2, 0x2, 0x8d, 0x8b, 0x3, 0x2, 0x2, 0x2, 0x8e, 0x90, 0x5, 
    0x12, 0xa, 0x2, 0x8f, 0x8e, 0x3, 0x2, 0x2, 0x2, 0x8f, 0x90, 0x3, 0x2, 
    0x2, 0x2, 0x90, 0x91, 0x3, 0x2, 0x2, 0x2, 0x91, 0x92, 0x9, 0x2, 0x2, 
    0x2, 0x92, 0x9, 0x3, 0x2, 0x2, 0x2, 0x93, 0x94, 0x6, 0x6, 0x4, 0x2, 
    0x94, 0x98, 0x5, 0xc, 0x7, 0x2, 0x95, 0x96, 0x6, 0x6, 0x5, 0x2, 0x96, 
    0x98, 0x5, 0x10, 0x9, 0x2, 0x97, 0x93, 0x3, 0x2, 0x2, 0x2, 0x97, 0x95, 
    0x3, 0x2, 0x2, 0x2, 0x98, 0xb, 0x3, 0x2, 0x2, 0x2, 0x99, 0x9e, 0x5, 
    0xe, 0x8, 0x2, 0x9a, 0x9b, 0x7, 0x24, 0x2, 0x2, 0x9b, 0x9d, 0x5, 0xe, 
    0x8, 0x2, 0x9c, 0x9a, 0x3, 0x2, 0x2, 0x2, 0x9d, 0xa0, 0x3, 0x2, 0x2, 
    0x2, 0x9e, 0x9c, 0x3, 0x2, 0x2, 0x2, 0x9e, 0x9f, 0x3, 0x2, 0x2, 0x2, 
    0x9f, 0xd, 0x3, 0x2, 0x2, 0x2, 0xa0, 0x9e, 0x3, 0x2, 0x2, 0x2, 0xa1, 
    0xa6, 0x5, 0x26, 0x14, 0x2, 0xa2, 0xa4, 0x7, 0x25, 0x2, 0x2, 0xa3, 0xa5, 
    0x5, 0x14, 0xb, 0x2, 0xa4, 0xa3, 0x3, 0x2, 0x2, 0x2, 0xa4, 0xa5, 0x3, 
    0x2, 0x2, 0x2, 0xa5, 0xa7, 0x3, 0x2, 0x2, 0x2, 0xa6, 0xa2, 0x3, 0x2, 
    0x2, 0x2, 0xa6, 0xa7, 0x3, 0x2, 0x2, 0x2, 0xa7, 0xf, 0x3, 0x2, 0x2, 
    0x2, 0xa8, 0xad, 0x5, 0x26, 0x14, 0x2, 0xa9, 0xaa, 0x7, 0x24, 0x2, 0x2, 
    0xaa, 0xac, 0x5, 0x26, 0x14, 0x2, 0xab, 0xa9, 0x3, 0x2, 0x2, 0x2, 0xac, 
    0xaf, 0x3, 0x2, 0x2, 0x2, 0xad, 0xab, 0x3, 0x2, 0x2, 0x2, 0xad, 0xae, 
    0x3, 0x2, 0x2, 0x2, 0xae, 0x11, 0x3, 0x2, 0x2, 0x2, 0xaf, 0xad, 0x3, 
    0x2, 0x2, 0x2, 0xb0, 0xb2, 0x7, 0x6, 0x2, 0x2, 0xb1, 0xb0, 0x3, 0x2, 
    0x2, 0x2, 0xb2, 0xb3, 0x3, 0x2, 0x2, 0x2, 0xb3, 0xb1, 0x3, 0x2, 0x2, 
    0x2, 0xb3, 0xb4, 0x3, 0x2, 0x2, 0x2, 0xb4, 0x13, 0x3, 0x2, 0x2, 0x2, 
    0xb5, 0xb7, 0x7, 0x6, 0x2, 0x2, 0xb6, 0xb5, 0x3, 0x2, 0x2, 0x2, 0xb7, 
    0xb8, 0x3, 0x2, 0x2, 0x2, 0xb8, 0xb6, 0x3, 0x2, 0x2, 0x2, 0xb8, 0xb9, 
    0x3, 0x2, 0x2, 0x2, 0xb9, 0x15, 0x3, 0x2, 0x2, 0x2, 0xba, 0xbd, 0x5, 
    0x18, 0xd, 0x2, 0xbb, 0xbd, 0x5, 0x1a, 0xe, 0x2, 0xbc, 0xba, 0x3, 0x2, 
    0x2, 0x2, 0xbc, 0xbb, 0x3, 0x2, 0x2, 0x2, 0xbd, 0x17, 0x3, 0x2, 0x2, 
    0x2, 0xbe, 0xbf, 0x7, 0xb, 0x2, 0x2, 0xbf, 0xc0, 0x5, 0x28, 0x15, 0x2, 
    0xc0, 0xc7, 0x5, 0x1e, 0x10, 0x2, 0xc1, 0xc2, 0x7, 0xc, 0x2, 0x2, 0xc2, 
    0xc3, 0x5, 0x28, 0x15, 0x2, 0xc3, 0xc4, 0x5, 0x1e, 0x10, 0x2, 0xc4, 
    0xc6, 0x3, 0x2, 0x2, 0x2, 0xc5, 0xc1, 0x3, 0x2, 0x2, 0x2, 0xc6, 0xc9, 
    0x3, 0x2, 0x2, 0x2, 0xc7, 0xc5, 0x3, 0x2, 0x2, 0x2, 0xc7, 0xc8, 0x3, 
    0x2, 0x2, 0x2, 0xc8, 0xcc, 0x3, 0x2, 0x2, 0x2, 0xc9, 0xc7, 0x3, 0x2, 
    0x2, 0x2, 0xca, 0xcb, 0x7, 0xd, 0x2, 0x2, 0xcb, 0xcd, 0x5, 0x1c, 0xf, 
    0x2, 0xcc, 0xca, 0x3, 0x2, 0x2, 0x2, 0xcc, 0xcd, 0x3, 0x2, 0x2, 0x2, 
    0xcd, 0xce, 0x3, 0x2, 0x2, 0x2, 0xce, 0xcf, 0x7, 0xe, 0x2, 0x2, 0xcf, 
    0x19, 0x3, 0x2, 0x2, 0x2, 0xd0, 0xd1, 0x7, 0xa, 0x2, 0x2, 0xd1, 0xd2, 
    0x5, 0x28, 0x15, 0x2, 0xd2, 0xd9, 0x5, 0x1e, 0x10, 0x2, 0xd3, 0xd4, 
    0x7, 0xc, 0x2, 0x2, 0xd4, 0xd5, 0x5, 0x28, 0x15, 0x2, 0xd5, 0xd6, 0x5, 
    0x1e, 0x10, 0x2, 0xd6, 0xd8, 0x3, 0x2, 0x2, 0x2, 0xd7, 0xd3, 0x3, 0x2, 
    0x2, 0x2, 0xd8, 0xdb, 0x3, 0x2, 0x2, 0x2, 0xd9, 0xd7, 0x3, 0x2, 0x2, 
    0x2, 0xd9, 0xda, 0x3, 0x2, 0x2, 0x2, 0xda, 0xde, 0x3, 0x2, 0x2, 0x2, 
    0xdb, 0xd9, 0x3, 0x2, 0x2, 0x2, 0xdc, 0xdd, 0x7, 0xd, 0x2, 0x2, 0xdd, 
    0xdf, 0x5, 0x1c, 0xf, 0x2, 0xde, 0xdc, 0x3, 0x2, 0x2, 0x2, 0xde, 0xdf, 
    0x3, 0x2, 0x2, 0x2, 0xdf, 0xe0, 0x3, 0x2, 0x2, 0x2, 0xe0, 0xe1, 0x7, 
    0xe, 0x2, 0x2, 0xe1, 0x1b, 0x3, 0x2, 0x2, 0x2, 0xe2, 0xe3, 0x5, 0x1e, 
    0x10, 0x2, 0xe3, 0x1d, 0x3, 0x2, 0x2, 0x2, 0xe4, 0xe6, 0x5, 0x4, 0x3, 
    0x2, 0xe5, 0xe4, 0x3, 0x2, 0x2, 0x2, 0xe6, 0xe9, 0x3, 0x2, 0x2, 0x2, 
    0xe7, 0xe5, 0x3, 0x2, 0x2, 0x2, 0xe7, 0xe8, 0x3, 0x2, 0x2, 0x2, 0xe8, 
    0x1f, 0x3, 0x2, 0x2, 0x2, 0xe9, 0xe7, 0x3, 0x2, 0x2, 0x2, 0xea, 0xfa, 
    0x7, 0x1e, 0x2, 0x2, 0xeb, 0xed, 0x7, 0x1d, 0x2, 0x2, 0xec, 0xee, 0x5, 
    0x22, 0x12, 0x2, 0xed, 0xec, 0x3, 0x2, 0x2, 0x2, 0xed, 0xee, 0x3, 0x2, 
    0x2, 0x2, 0xee, 0xf5, 0x3, 0x2, 0x2, 0x2, 0xef, 0xf1, 0x7, 0x24, 0x2, 
    0x2, 0xf0, 0xf2, 0x5, 0x22, 0x12, 0x2, 0xf1, 0xf0, 0x3, 0x2, 0x2, 0x2, 
    0xf1, 0xf2, 0x3, 0x2, 0x2, 0x2, 0xf2, 0xf4, 0x3, 0x2, 0x2, 0x2, 0xf3, 
    0xef, 0x3, 0x2, 0x2, 0x2, 0xf4, 0xf7, 0x3, 0x2, 0x2, 0x2, 0xf5, 0xf3, 
    0x3, 0x2, 0x2, 0x2, 0xf5, 0xf6, 0x3, 0x2, 0x2, 0x2, 0xf6, 0xf8, 0x3, 
    0x2, 0x2, 0x2, 0xf7, 0xf5, 0x3, 0x2, 0x2, 0x2, 0xf8, 0xfa, 0x7, 0x23, 
    0x2, 0x2, 0xf9, 0xea, 0x3, 0x2, 0x2, 0x2, 0xf9, 0xeb, 0x3, 0x2, 0x2, 
    0x2, 0xfa, 0x21, 0x3, 0x2, 0x2, 0x2, 0xfb, 0xfd, 0x5, 0x4, 0x3, 0x2, 
    0xfc, 0xfb, 0x3, 0x2, 0x2, 0x2, 0xfd, 0xfe, 0x3, 0x2, 0x2, 0x2, 0xfe, 
    0xfc, 0x3, 0x2, 0x2, 0x2, 0xfe, 0xff, 0x3, 0x2, 0x2, 0x2, 0xff, 0x23, 
    0x3, 0x2, 0x2, 0x2, 0x100, 0x101, 0x7, 0x28, 0x2, 0x2, 0x101, 0x25, 
    0x3, 0x2, 0x2, 0x2, 0x102, 0x104, 0x7, 0x5, 0x2, 0x2, 0x103, 0x102, 
    0x3, 0x2, 0x2, 0x2, 0x104, 0x107, 0x3, 0x2, 0x2, 0x2, 0x105, 0x103, 
    0x3, 0x2, 0x2, 0x2, 0x105, 0x106, 0x3, 0x2, 0x2, 0x2, 0x106, 0x108, 
    0x3, 0x2, 0x2, 0x2, 0x107, 0x105, 0x3, 0x2, 0x2, 0x2, 0x108, 0x10c, 
    0x7, 0x28, 0x2, 0x2, 0x109, 0x10b, 0x7, 0x5, 0x2, 0x2, 0x10a, 0x109, 
    0x3, 0x2, 0x2, 0x2, 0x10b, 0x10e, 0x3, 0x2, 0x2, 0x2, 0x10c, 0x10a, 
    0x3, 0x2, 0x2, 0x2, 0x10c, 0x10d, 0x3, 0x2, 0x2, 0x2, 0x10d, 0x27, 0x3, 
    0x2, 0x2, 0x2, 0x10e, 0x10c, 0x3, 0x2, 0x2, 0x2, 0x10f, 0x110, 0x7, 
    0x28, 0x2, 0x2, 0x110, 0x29, 0x3, 0x2, 0x2, 0x2, 0x111, 0x112, 0x7, 
    0xf, 0x2, 0x2, 0x112, 0x113, 0x7, 0x28, 0x2, 0x2, 0x113, 0x114, 0x9, 
    0x3, 0x2, 0x2, 0x114, 0x2b, 0x3, 0x2, 0x2, 0x2, 0x115, 0x116, 0x7, 0x15, 
    0x2, 0x2, 0x116, 0x2d, 0x3, 0x2, 0x2, 0x2, 0x117, 0x118, 0x7, 0x16, 
    0x2, 0x2, 0x118, 0x2f, 0x3, 0x2, 0x2, 0x2, 0x119, 0x11a, 0x7, 0x1a, 
    0x2, 0x2, 0x11a, 0x31, 0x3, 0x2, 0x2, 0x2, 0x11b, 0x11c, 0x7, 0x1b, 
    0x2, 0x2, 0x11c, 0x33, 0x3, 0x2, 0x2, 0x2, 0x11d, 0x11e, 0x7, 0x18, 
    0x2, 0x2, 0x11e, 0x11f, 0x5, 0x36, 0x1c, 0x2, 0x11f, 0x35, 0x3, 0x2, 
    0x2, 0x2, 0x120, 0x12e, 0x7, 0x30, 0x2, 0x2, 0x121, 0x12e, 0x7, 0x31, 
    0x2, 0x2, 0x122, 0x12e, 0x7, 0x32, 0x2, 0x2, 0x123, 0x12e, 0x7, 0x33, 
    0x2, 0x2, 0x124, 0x12e, 0x7, 0x34, 0x2, 0x2, 0x125, 0x12e, 0x7, 0x35, 
    0x2, 0x2, 0x126, 0x12e, 0x7, 0x36, 0x2, 0x2, 0x127, 0x12e, 0x7, 0x37, 
    0x2, 0x2, 0x128, 0x12e, 0x7, 0x38, 0x2, 0x2, 0x129, 0x12e, 0x7, 0x39, 
    0x2, 0x2, 0x12a, 0x12e, 0x7, 0x3a, 0x2, 0x2, 0x12b, 0x12c, 0x6, 0x1c, 
    0x6, 0x2, 0x12c, 0x12e, 0x7, 0x39, 0x2, 0x2, 0x12d, 0x120, 0x3, 0x2, 
    0x2, 0x2, 0x12d, 0x121, 0x3, 0x2, 0x2, 0x2, 0x12d, 0x122, 0x3, 0x2, 
    0x2, 0x2, 0x12d, 0x123, 0x3, 0x2, 0x2, 0x2, 0x12d, 0x124, 0x3, 0x2, 
    0x2, 0x2, 0x12d, 0x125, 0x3, 0x2, 0x2, 0x2, 0x12d, 0x126, 0x3, 0x2, 
    0x2, 0x2, 0x12d, 0x127, 0x3, 0x2, 0x2, 0x2, 0x12d, 0x128, 0x3, 0x2, 
    0x2, 0x2, 0x12d, 0x129, 0x3, 0x2, 0x2, 0x2, 0x12d, 0x12a, 0x3, 0x2, 
    0x2, 0x2, 0x12d, 0x12b, 0x3, 0x2, 0x2, 0x2, 0x12e, 0x37, 0x3, 0x2, 0x2, 
    0x2, 0x12f, 0x130, 0x7, 0x19, 0x2, 0x2, 0x130, 0x131, 0x7, 0x2f, 0x2, 
    0x2, 0x131, 0x132, 0x7, 0x3, 0x2, 0x2, 0x132, 0x133, 0x7, 0x2f, 0x2, 
    0x2, 0x133, 0x39, 0x3, 0x2, 0x2, 0x2, 0x134, 0x135, 0x7, 0x17, 0x2, 
    0x2, 0x135, 0x136, 0x7, 0x3c, 0x2, 0x2, 0x136, 0x137, 0x7, 0x3d, 0x2, 
    0x2, 0x137, 0x138, 0x7, 0x3c, 0x2, 0x2, 0x138, 0x3b, 0x3, 0x2, 0x2, 
    0x2, 0x139, 0x13d, 0x7, 0x1c, 0x2, 0x2, 0x13a, 0x13c, 0x7, 0x44, 0x2, 
    0x2, 0x13b, 0x13a, 0x3, 0x2, 0x2, 0x2, 0x13c, 0x13f, 0x3, 0x2, 0x2, 
    0x2, 0x13d, 0x13b, 0x3, 0x2, 0x2, 0x2, 0x13d, 0x13e, 0x3, 0x2, 0x2, 
    0x2, 0x13e, 0x140, 0x3, 0x2, 0x2, 0x2, 0x13f, 0x13d, 0x3, 0x2, 0x2, 
    0x2, 0x140, 0x141, 0x7, 0x43, 0x2, 0x2, 0x141, 0x3d, 0x3, 0x2, 0x2, 
    0x2, 0x142, 0x143, 0x7, 0x14, 0x2, 0x2, 0x143, 0x3f, 0x3, 0x2, 0x2, 
    0x2, 0x144, 0x145, 0x7, 0x13, 0x2, 0x2, 0x145, 0x41, 0x3, 0x2, 0x2, 
    0x2, 0x146, 0x147, 0x7, 0x10, 0x2, 0x2, 0x147, 0x148, 0x5, 0x44, 0x23, 
    0x2, 0x148, 0x43, 0x3, 0x2, 0x2, 0x2, 0x149, 0x14a, 0x7, 0x3, 0x2, 0x2, 
    0x14a, 0x45, 0x3, 0x2, 0x2, 0x2, 0x14b, 0x14c, 0x7, 0x11, 0x2, 0x2, 
    0x14c, 0x47, 0x3, 0x2, 0x2, 0x2, 0x14d, 0x151, 0x7, 0x8, 0x2, 0x2, 0x14e, 
    0x152, 0x7, 0x3, 0x2, 0x2, 0x14f, 0x150, 0x6, 0x25, 0x7, 0x2, 0x150, 
    0x152, 0x5, 0x20, 0x11, 0x2, 0x151, 0x14e, 0x3, 0x2, 0x2, 0x2, 0x151, 
    0x14f, 0x3, 0x2, 0x2, 0x2, 0x152, 0x49, 0x3, 0x2, 0x2, 0x2, 0x153, 0x154, 
    0x7, 0x12, 0x2, 0x2, 0x154, 0x15d, 0x5, 0x4c, 0x27, 0x2, 0x155, 0x15a, 
    0x5, 0x4e, 0x28, 0x2, 0x156, 0x157, 0x7, 0x24, 0x2, 0x2, 0x157, 0x159, 
    0x5, 0x4e, 0x28, 0x2, 0x158, 0x156, 0x3, 0x2, 0x2, 0x2, 0x159, 0x15c, 
    0x3, 0x2, 0x2, 0x2, 0x15a, 0x158, 0x3, 0x2, 0x2, 0x2, 0x15a, 0x15b, 
    0x3, 0x2, 0x2, 0x2, 0x15b, 0x15e, 0x3, 0x2, 0x2, 0x2, 0x15c, 0x15a, 
    0x3, 0x2, 0x2, 0x2, 0x15d, 0x155, 0x3, 0x2, 0x2, 0x2, 0x15d, 0x15e, 
    0x3, 0x2, 0x2, 0x2, 0x15e, 0x15f, 0x3, 0x2, 0x2, 0x2, 0x15f, 0x160, 
    0x9, 0x4, 0x2, 0x2, 0x160, 0x4b, 0x3, 0x2, 0x2, 0x2, 0x161, 0x162, 0x7, 
    0x28, 0x2, 0x2, 0x162, 0x4d, 0x3, 0x2, 0x2, 0x2, 0x163, 0x16a, 0x5, 
    0x52, 0x2a, 0x2, 0x164, 0x165, 0x5, 0x52, 0x2a, 0x2, 0x165, 0x166, 0x7, 
    0x25, 0x2, 0x2, 0x166, 0x167, 0x5, 0x50, 0x29, 0x2, 0x167, 0x16a, 0x3, 
    0x2, 0x2, 0x2, 0x168, 0x16a, 0x5, 0x50, 0x29, 0x2, 0x169, 0x163, 0x3, 
    0x2, 0x2, 0x2, 0x169, 0x164, 0x3, 0x2, 0x2, 0x2, 0x169, 0x168, 0x3, 
    0x2, 0x2, 0x2, 0x16a, 0x4f, 0x3, 0x2, 0x2, 0x2, 0x16b, 0x16c, 0x7, 0x22, 
    0x2, 0x2, 0x16c, 0x171, 0x5, 0x4e, 0x28, 0x2, 0x16d, 0x16e, 0x7, 0x24, 
    0x2, 0x2, 0x16e, 0x170, 0x5, 0x4e, 0x28, 0x2, 0x16f, 0x16d, 0x3, 0x2, 
    0x2, 0x2, 0x170, 0x173, 0x3, 0x2, 0x2, 0x2, 0x171, 0x16f, 0x3, 0x2, 
    0x2, 0x2, 0x171, 0x172, 0x3, 0x2, 0x2, 0x2, 0x172, 0x174, 0x3, 0x2, 
    0x2, 0x2, 0x173, 0x171, 0x3, 0x2, 0x2, 0x2, 0x174, 0x175, 0x7, 0x23, 
    0x2, 0x2, 0x175, 0x17a, 0x3, 0x2, 0x2, 0x2, 0x176, 0x17a, 0x7, 0x2f, 
    0x2, 0x2, 0x177, 0x17a, 0x7, 0x3, 0x2, 0x2, 0x178, 0x17a, 0x7, 0x28, 
    0x2, 0x2, 0x179, 0x16b, 0x3, 0x2, 0x2, 0x2, 0x179, 0x176, 0x3, 0x2, 
    0x2, 0x2, 0x179, 0x177, 0x3, 0x2, 0x2, 0x2, 0x179, 0x178, 0x3, 0x2, 
    0x2, 0x2, 0x17a, 0x51, 0x3, 0x2, 0x2, 0x2, 0x17b, 0x17c, 0x7, 0x28, 
    0x2, 0x2, 0x17c, 0x53, 0x3, 0x2, 0x2, 0x2, 0x26, 0x57, 0x65, 0x7b, 0x7d, 
    0x83, 0x86, 0x8b, 0x8f, 0x97, 0x9e, 0xa4, 0xa6, 0xad, 0xb3, 0xb8, 0xbc, 
    0xc7, 0xcc, 0xd9, 0xde, 0xe7, 0xed, 0xf1, 0xf5, 0xf9, 0xfe, 0x105, 0x10c, 
    0x12d, 0x13d, 0x151, 0x15a, 0x15d, 0x169, 0x171, 0x179, 
  };

  atn::ATNDeserializer deserializer;
  _atn = deserializer.deserialize(_serializedATN);

  size_t count = _atn.getNumberOfDecisions();
  _decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    _decisionToDFA.emplace_back(_atn.getDecisionState(i), i);
  }
}

verilogPreprocParser::Initializer verilogPreprocParser::_init;
