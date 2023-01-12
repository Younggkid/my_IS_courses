/****************************************************/
/* File: parse.c                                    */
/* The parser implementation for the TINY compiler  */
/* Compiler Construction: Principles and Practice   */
/* Kenneth C. Louden                                */
/****************************************************/

#include "globals.h"
#include "util.h"
#include "lexer.h"
#include "parse.h"

static TokenType token; /* holds current token */

/* function prototypes for recursive calls */
static TreeNode * stmt_sequence(void);
static TreeNode * statement(void);
static TreeNode * if_stmt(void);
static TreeNode * repeat_stmt(void);
static TreeNode * assign_stmt(void);
static TreeNode * read_stmt(void);
static TreeNode * write_stmt(void);
static TreeNode * exp(void);
static TreeNode * simple_exp(void);
static TreeNode * term(void);
static TreeNode * factor(void);

static void syntaxError(char * message)
{ fprintf(listing,"\n>>> ");
  fprintf(listing,"Syntax error at line %d: %s",lineno,message);
  Error = TRUE;
}

/* This fuction can be called by the following fuctions. */
static void match(TokenType expected) 
{ if (token == expected) token = getToken();
  else {
    syntaxError("unexpected token -> ");
    printToken(token,tokenString);
    fprintf(listing,"      ");
  }
}


/* Each of the following functions represents the process of put one certain non-terminal character on the syntex tree as a node: */
/* You can write other functions referring to the format of the function  stmt_sequence(void). */

TreeNode * stmt_sequence(void)
{ TreeNode * t = statement();
  TreeNode * p = t;
  while ((token!=ENDFILE) && (token!=END) &&
         (token!=ELSE) && (token!=UNTIL))
  { TreeNode * q;
    //match(SEMI);
    q = statement();
    if (q!=NULL) {
      if (t==NULL) t = p = q;
      else /* now p cannot be NULL either */
      { p->sibling = q;
        p = q;
      }
    }
  }
  return t;
}
//采用递归下降分析法，为每个非终结符定义一个函数
TreeNode * statement(void)
{
  TreeNode * t = NULL;
  switch(token)
  {
    case IF: t = if_stmt(); break;
    case REPEAT : t = repeat_stmt(); break;
    case ID : t = assign_stmt(); break;
    case READ : t = read_stmt(); break;
    case WRITE : t = write_stmt(); break;
 }
  return t;
}

TreeNode * repeat_stmt(void)//对repeat分析，repeat有两个儿子结点
{
  TreeNode * t = newStmtNode(RepeatK);
  if(t == NULL) return t;
  match(REPEAT);
  t ->child[0] = stmt_sequence();
  match(UNTIL);
  t -> child[1] = exp();
  return t;
}

TreeNode * if_stmt(void)//对if子句分析，repeat有两个或三个儿子结点
{ 
  TreeNode * t = newStmtNode(IfK);
  if(t == NULL) return t;
  match(IF);
  t -> child[0] = exp();
  match(THEN);
  t -> child[1] = stmt_sequence();
  if(token == ELSE)
  {
    match(ELSE);
    t -> child[2] = stmt_sequence();
  }
  match(END);
  return t;
}


TreeNode * assign_stmt(void)//对赋值语句分析，要把左侧变量取出来并把表达式子树付给唯一的儿子
{ 
  TreeNode * t = newStmtNode(AssignK);
  if(t == NULL) return t;
  t->attr.name = copyString(tokenString);
  if(token == ID)
  { match(ID);
    match(ASSIGN);
  t->child[0] = exp();
  }
  return t;

  
}

TreeNode * read_stmt(void)//read没有儿子，只需把后面的变量名拿到就行
{ 
  TreeNode * t = newStmtNode(ReadK);
  match(READ);
  if((t!=NULL)&&(token==ID)){
        t->attr.name = copyString(tokenString);
    }
  match(ID);
  return t;
}

TreeNode * write_stmt(void)//write把后面的表达式子树付给儿子
{ 
  TreeNode * t = newStmtNode(WriteK);
  if(t == NULL) return t;
  match(WRITE);
  t ->child[0] = exp();
  return t;
}

TreeNode * exp(void)
{ 
  //exp右侧一定会有simple'exp，先进行分析
  TreeNode * t = simple_exp();
  //如果发现有cop，则说明后面还有simple'exp
  //把cop作为返回结点，两个儿子链接左右两个simple’exp
  if(token == EQ || token == LT )
  {
    TreeNode * q = newExpNode(OpK);
    q ->attr.op = token;
    match(token);
    q -> child[0] = t;
    q -> child[1] = simple_exp();
    return q;
  }
  return t;
}
//接下来文法中存在左递归，可以用BNF解决
TreeNode * simple_exp(void)
{
 TreeNode * t = term();
    while ((token == PLUS)||(token == MINUS)){ 
        TreeNode * p = newExpNode(OpK);
        if (p!=NULL) {
            p->child[0] = t;
            p->attr.op = token;
            t = p;
            match(token);
            t->child[1] = term();
        }
    }
    return t;

}

TreeNode * term(void)
{ 
  TreeNode * t = factor();
    while ((token == TIMES)||(token == OVER)){
        TreeNode * p = newExpNode(OpK);
        if (p!=NULL){
            p->child[0] = t;
            p->attr.op = token;
            t = p;
            match(token);
            p->child[1] = factor();
        }
    }
    return t;
}

TreeNode * factor(void)
{ 
  if(token == NUM)
  {
    TreeNode * t = newExpNode(ConstK);
    t->attr.val = atoi(tokenString);
    match(token);
    return t;
  }
  else if(token == ID)
  {
    TreeNode * t = newExpNode(IdK);
    t->attr.name = copyString(tokenString);
    match(token);
    return t;
  }
  else if(token == LPAREN)
  {
    match(token);
    TreeNode * t = exp();
    match(RPAREN);
    return t;
  }
  
}


/****************************************/
/* the primary function of the parser   */
/****************************************/
/* Function parse returns the newly
 * constructed syntax tree
 */
TreeNode * parse(void)
{ TreeNode * t;
  token = getToken(); /*get one token each time and parse it */
  t = stmt_sequence();
  if (token!=ENDFILE)
    syntaxError("Code ends before file\n");
  return t;
}
