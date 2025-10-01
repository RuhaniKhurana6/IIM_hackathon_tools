import openai
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class EnhancedChatbot:
    def __init__(self):
        self.conversation_history = []
        self.user_data = {}
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
    def chat(self, user_id, message):
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Provide detailed answers to any questions."
                },
                {"role": "user", "content": message}
            ]
            
            history = self.get_recent_history(user_id)
            messages.extend(history)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=1
            )
            
            response_text = response.choices[0].message.content
            self.store_conversation(user_id, message, response_text)
            
            return response_text
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"

    # Add helper methods here
    # ...existing code...

    def get_recent_history(self, user_id):
        """Retrieve recent conversation history for a specific user."""
        return self.conversation_history.get(user_id, [])[-5:]

    def store_conversation(self, user_id, user_message, bot_response):
        """Store conversation history for a specific user."""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        self.conversation_history[user_id].append({
            "user": user_message,
            "bot": bot_response,
            "timestamp": datetime.now().isoformat()
        })





import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Try to import pandas, but make it optional
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("Warning: pandas not available. Some features will be limited.")

# Try to import LangChain components, but make them optional
try:
    from langchain.llms import OpenAI
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.memory import ConversationBufferWindowMemory
    from langchain.chains import ConversationalRetrievalChain
    from langchain.schema import Document
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False
    print("Warning: LangChain not available. Using mock responses only.")

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

class TaxChatbot:
    """
    Comprehensive AI Chatbot for Tax Helper Application
    Can analyze user data and answer any questions about their financial/tax information
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key or not HAS_LANGCHAIN:
            if not self.api_key:
                logging.warning("OpenAI API key not found. Using mock responses.")
            if not HAS_LANGCHAIN:
                logging.warning("LangChain not available. Using mock responses.")
            self.use_mock = True
        else:
            self.use_mock = False
            
        self.user_data = {}
        self.conversation_history = []
        self.vector_store = None
        
        if HAS_LANGCHAIN and not self.use_mock:
            self.memory = ConversationBufferWindowMemory(
                memory_key="chat_history",
                return_messages=True,
                k=10  # Keep last 10 interactions
            )
            self.llm = OpenAI(
                api_key=self.api_key,
                temperature=0.7,
                max_tokens=500
            )
            self.embeddings = OpenAIEmbeddings(api_key=self.api_key)
        else:
            self.memory = None
            self.llm = None
            self.embeddings = None
            
        self.setup_tax_knowledge_base()
    
    def setup_tax_knowledge_base(self):
        """Setup knowledge base with tax information and user data context"""
        tax_knowledge = [
            """
            Tax Deductible Business Expenses:
            - Office supplies and equipment
            - Business travel and transportation
            - Professional development and training
            - Business meals (50% deductible)
            - Home office expenses
            - Professional services (legal, accounting)
            - Software and technology expenses
            - Marketing and advertising costs
            """,
            """
            Non-Deductible Personal Expenses:
            - Personal meals and entertainment
            - Personal travel and vacations
            - Personal clothing and grooming
            - Personal medical expenses (unless exceeding threshold)
            - Personal insurance premiums
            - Personal investment expenses
            """,
            """
            Tax Planning Tips:
            - Keep detailed records of all business expenses
            - Separate business and personal expenses clearly
            - Save receipts and documentation
            - Consider timing of expenses for tax optimization
            - Maximize retirement contributions
            - Use tax-advantaged accounts when possible
            """
        ]
        
        if not self.use_mock and HAS_LANGCHAIN:
            try:
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                
                documents = []
                for knowledge in tax_knowledge:
                    chunks = text_splitter.split_text(knowledge)
                    for chunk in chunks:
                        documents.append(Document(page_content=chunk))
                
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
            except Exception as e:
                logging.error(f"Failed to setup vector store: {e}")
                self.use_mock = True
    
    def update_user_data(self, user_id: str, data: Dict[str, Any]):
        """Update user-specific data for personalized responses"""
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                'transactions': [],
                'categories': {},
                'tax_summary': {},
                'preferences': {},
                'last_updated': datetime.now().isoformat()
            }
        
        # Update with new data
        for key, value in data.items():
            self.user_data[user_id][key] = value
        
        self.user_data[user_id]['last_updated'] = datetime.now().isoformat()
        
        # Update vector store with user data if not using mock
        if not self.use_mock and self.vector_store:
            self._update_vector_store_with_user_data(user_id)
    
    def _update_vector_store_with_user_data(self, user_id: str):
        """Update vector store with user-specific data"""
        user_info = self.user_data.get(user_id, {})
        
        # Create documents from user data
        user_documents = []
        
        # Add transaction data
        transactions = user_info.get('transactions', [])
        if transactions:
            transaction_summary = f"User's recent transactions: {json.dumps(transactions[:20])}"
            user_documents.append(Document(page_content=transaction_summary))
        
        # Add category information
        categories = user_info.get('categories', {})
        if categories:
            category_summary = f"User's expense categories: {json.dumps(categories)}"
            user_documents.append(Document(page_content=category_summary))
        
        # Add tax summary
        tax_summary = user_info.get('tax_summary', {})
        if tax_summary:
            summary_text = f"User's tax summary: {json.dumps(tax_summary)}"
            user_documents.append(Document(page_content=summary_text))
        
        # Add to vector store
        if user_documents:
            try:
                new_vector_store = FAISS.from_documents(user_documents, self.embeddings)
                # Merge with existing vector store
                self.vector_store.merge_from(new_vector_store)
            except Exception as e:
                logging.error(f"Failed to update vector store with user data: {e}")
    
    def analyze_user_data(self, user_id: str) -> Dict[str, Any]:
        """Analyze user data and provide insights"""
        if user_id not in self.user_data:
            return {"error": "No data found for user"}
        
        user_info = self.user_data[user_id]
        transactions = user_info.get('transactions', [])
        
        if not transactions:
            return {
                "message": "No transaction data available for analysis",
                "recommendations": [
                    "Upload your transaction data to get personalized insights",
                    "Connect your bank account for automatic categorization",
                    "Start tracking your business expenses"
                ]
            }
        
        # Analyze transactions
        analysis = {
            "total_transactions": len(transactions),
            "total_amount": sum(t.get('amount', 0) for t in transactions),
            "deductible_amount": 0,
            "non_deductible_amount": 0,
            "categories": {},
            "monthly_breakdown": {},
            "top_merchants": {},
            "recommendations": []
        }
        
        if HAS_PANDAS:
            # Use pandas for advanced analysis
            df = pd.DataFrame(transactions)
            
            # Category analysis
            if 'category' in df.columns:
                category_counts = df['category'].value_counts()
                analysis['categories'] = category_counts.to_dict()
                
                # Calculate deductible vs non-deductible
                if 'tax_deductible' in df.columns:
                    deductible_df = df[df['tax_deductible'] == True]
                    non_deductible_df = df[df['tax_deductible'] == False]
                    
                    analysis['deductible_amount'] = deductible_df.get('amount', pd.Series()).sum()
                    analysis['non_deductible_amount'] = non_deductible_df.get('amount', pd.Series()).sum()
            
            # Monthly breakdown
            if 'date' in df.columns:
                df['month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
                monthly_spending = df.groupby('month')['amount'].sum()
                analysis['monthly_breakdown'] = monthly_spending.to_dict()
            
            # Top merchants
            if 'description' in df.columns:
                merchant_spending = df.groupby('description')['amount'].sum().sort_values(ascending=False)
                analysis['top_merchants'] = merchant_spending.head(5).to_dict()
        else:
            # Manual analysis without pandas
            categories = {}
            merchants = {}
            monthly = {}
            
            for t in transactions:
                # Category analysis
                cat = t.get('category', 'Uncategorized')
                categories[cat] = categories.get(cat, 0) + 1
                
                # Deductible analysis
                if t.get('tax_deductible', False):
                    analysis['deductible_amount'] += t.get('amount', 0)
                else:
                    analysis['non_deductible_amount'] += t.get('amount', 0)
                
                # Merchant analysis
                desc = t.get('description', 'Unknown')
                merchants[desc] = merchants.get(desc, 0) + t.get('amount', 0)
                
                # Monthly analysis (simplified)
                date_str = t.get('date', '2023-01-01')
                month = date_str[:7] if len(date_str) >= 7 else '2023-01'  # Extract YYYY-MM
                monthly[month] = monthly.get(month, 0) + t.get('amount', 0)
            
            analysis['categories'] = categories
            analysis['top_merchants'] = dict(sorted(merchants.items(), key=lambda x: x[1], reverse=True)[:5])
            analysis['monthly_breakdown'] = monthly
        
        # Generate recommendations
        recommendations = []
        if analysis['deductible_amount'] > 0:
            tax_savings = analysis['deductible_amount'] * 0.25  # Assuming 25% tax bracket
            recommendations.append(f"You could save approximately ${tax_savings:.2f} in taxes from your deductible expenses")
        
        if analysis['non_deductible_amount'] > analysis['deductible_amount']:
            recommendations.append("Consider tracking more business expenses to maximize your tax deductions")
        
        recommendations.extend([
            "Keep detailed records of all business-related expenses",
            "Consider using a business credit card for easier expense tracking",
            "Review your expenses monthly to identify tax-saving opportunities"
        ])
        
        analysis['recommendations'] = recommendations
        return analysis
    
    def chat(self, user_id: str, message: str) -> str:
        """Main chat function that can answer any question about user's data"""
        
        # Store conversation
        self.conversation_history.append({
            'user_id': user_id,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # If using mock mode, provide intelligent mock responses
        if self.use_mock:
            return self._generate_mock_response(user_id, message)
        
        try:
            # Get user context
            user_context = self._get_user_context(user_id, message)
            
            # Create enhanced prompt with user data
            enhanced_message = f"""
            User Question: {message}
            
            User Context: {user_context}
            
            You are a helpful AI tax assistant. Use the user's data to provide personalized, 
            accurate responses about their tax situation, expenses, and financial insights. 
            If you don't have specific data, provide general tax advice and suggest how they 
            can better track their information.
            """
            
            # Use conversational retrieval chain if vector store is available
            if self.vector_store:
                qa_chain = ConversationalRetrievalChain.from_llm(
                    self.llm,
                    retriever=self.vector_store.as_retriever(),
                    memory=self.memory,
                    return_source_documents=False
                )
                response = qa_chain({"question": enhanced_message})
                return response['answer']
            else:
                # Direct LLM call
                response = self.llm(enhanced_message)
                return response
                
        except Exception as e:
            logging.error(f"Error in chat function: {e}")
            return self._generate_mock_response(user_id, message)
    
    def _get_user_context(self, user_id: str, message: str) -> str:
        """Get relevant user context based on the message"""
        if user_id not in self.user_data:
            return "No user data available."
        
        user_info = self.user_data[user_id]
        context_parts = []
        
        # Always include basic summary
        if 'tax_summary' in user_info:
            context_parts.append(f"Tax Summary: {json.dumps(user_info['tax_summary'])}")
        
        # Include transaction data if relevant
        message_lower = message.lower()
        if any(keyword in message_lower for keyword in ['transaction', 'expense', 'spending', 'money', 'amount']):
            transactions = user_info.get('transactions', [])[:10]  # Latest 10
            if transactions:
                context_parts.append(f"Recent Transactions: {json.dumps(transactions)}")
        
        # Include category data if relevant
        if any(keyword in message_lower for keyword in ['category', 'type', 'business', 'personal']):
            categories = user_info.get('categories', {})
            if categories:
                context_parts.append(f"Expense Categories: {json.dumps(categories)}")
        
        return "\n".join(context_parts) if context_parts else "Limited user data available."
    
    def _generate_mock_response(self, user_id: str, message: str) -> str:
        """Generate intelligent mock responses when OpenAI API is not available"""
        message_lower = message.lower()
        
        # Get user data for personalized mock responses
        user_info = self.user_data.get(user_id, {})
        transactions = user_info.get('transactions', [])
        tax_summary = user_info.get('tax_summary', {})
        
        # Greeting responses
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'start']):
            return f"Hello! I'm your AI tax assistant. I can help you understand your tax situation, categorize expenses, and provide personalized financial insights. I have access to {len(transactions)} of your transactions. What would you like to know?"
        
        # Tax deduction questions
        elif 'deduct' in message_lower or 'tax' in message_lower:
            if tax_summary:
                deductible = tax_summary.get('total_deductible', 0)
                return f"Based on your data, you have ${deductible} in tax-deductible expenses. This includes business expenses like office supplies, professional services, and business travel. Would you like me to explain which specific expenses are deductible?"
            else:
                return "Tax deductions can significantly reduce your tax liability. Business expenses like office supplies, professional development, business travel, and home office expenses are typically deductible. I can help you identify which of your expenses qualify!"
        
        # Expense/spending questions
        elif any(word in message_lower for word in ['expense', 'spending', 'money', 'cost']):
            if transactions:
                total = sum(t.get('amount', 0) for t in transactions)
                business_expenses = [t for t in transactions if t.get('tax_deductible', False)]
                business_total = sum(t.get('amount', 0) for t in business_expenses)
                
                return f"You have ${total} in total expenses from {len(transactions)} transactions. Of these, ${business_total} are business expenses that may be tax-deductible. Your top spending categories appear to be related to your business operations."
            else:
                return "I don't have your expense data yet. Upload your transaction data or connect your bank account so I can provide personalized spending insights and identify potential tax deductions."
        
        # Category questions
        elif 'categor' in message_lower or 'type' in message_lower:
            if transactions:
                categories = {}
                for t in transactions:
                    cat = t.get('category', 'Uncategorized')
                    categories[cat] = categories.get(cat, 0) + t.get('amount', 0)
                
                cat_summary = ", ".join([f"{cat}: ${amount}" for cat, amount in categories.items()])
                return f"Your expenses are categorized as follows: {cat_summary}. I can help you optimize these categories for better tax planning."
            else:
                return "I categorize expenses into business and personal types. Business expenses are typically tax-deductible while personal expenses are not. Upload your data so I can categorize your specific transactions."
        
        # Summary/overview questions
        elif any(word in message_lower for word in ['summary', 'overview', 'total', 'how much']):
            if tax_summary:
                return f"Here's your tax summary: Total deductible expenses: ${tax_summary.get('total_deductible', 0)}, Potential tax savings: ${tax_summary.get('potential_savings', 0)}, Total transactions analyzed: {len(transactions)}. This data can help you make informed tax decisions."
            else:
                return "I can provide a comprehensive summary of your tax situation including deductible expenses, potential savings, and spending patterns. Upload your transaction data to get started!"
        
        # Help questions
        elif 'help' in message_lower or 'can you' in message_lower:
            return "I can help you with: 1) Identifying tax-deductible expenses, 2) Categorizing your transactions, 3) Calculating potential tax savings, 4) Providing tax planning advice, 5) Analyzing your spending patterns, 6) Answering specific questions about your financial data. What would you like to explore?"
        
        # Default intelligent response
        else:
            data_context = f"I have access to {len(transactions)} of your transactions" if transactions else "I don't have your transaction data yet"
            return f"I'm here to help with your tax and financial questions! {data_context}. I can analyze your expenses, identify tax deductions, provide personalized advice, and answer any questions about your financial data. Could you please rephrase your question or ask something specific about your taxes or expenses?"
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for a user"""
        user_conversations = [
            conv for conv in self.conversation_history 
            if conv['user_id'] == user_id
        ]
        return user_conversations[-limit:]
    
    def clear_conversation_history(self, user_id: str):
        """Clear conversation history for a user"""
        self.conversation_history = [
            conv for conv in self.conversation_history 
            if conv['user_id'] != user_id
        ]
        if self.memory:
            self.memory.clear()
    
    def get_personalized_insights(self, user_id: str) -> List[str]:
        """Generate personalized insights based on user data"""
        analysis = self.analyze_user_data(user_id)
        
        if 'error' in analysis:
            return [
                "Connect your financial accounts to get personalized insights",
                "Start tracking your business expenses for better tax planning",
                "Upload receipts to maximize your tax deductions"
            ]
        
        insights = []
        
        # Tax savings insights
        if analysis['deductible_amount'] > 0:
            savings = analysis['deductible_amount'] * 0.25
            insights.append(f"You could save approximately ${savings:.2f} in taxes this year")
        
        # Spending pattern insights
        if analysis['categories']:
            top_category = max(analysis['categories'], key=analysis['categories'].get)
            insights.append(f"Your highest expense category is '{top_category}'")
        
        # Monthly insights
        if analysis['monthly_breakdown']:
            months = list(analysis['monthly_breakdown'].keys())
            if len(months) >= 2:
                latest_month = max(months)
                latest_spending = analysis['monthly_breakdown'][latest_month]
                insights.append(f"Your spending in {latest_month} was ${latest_spending}")
        
        # Add recommendations
        insights.extend(analysis.get('recommendations', [])[:3])
        
        return insights


# Global instance
chatbot_instance = TaxChatbot()

def get_chatbot() -> TaxChatbot:
    """Get the global chatbot instance"""
    return chatbot_instance