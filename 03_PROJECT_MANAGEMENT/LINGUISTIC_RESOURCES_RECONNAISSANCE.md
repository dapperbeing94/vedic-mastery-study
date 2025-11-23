# Linguistic Resources Reconnaissance

## 🎯 **Mission**: Find Hard Linguistic Resources for Internal Knowledge Base

---

## 🏆 **GOLDMINE DISCOVERED: Sanskrit Lexicon Organization**

**URL**: https://github.com/sanskrit-lexicon  
**Description**: Cologne Digital Sanskrit Dictionaries Backend  
**Repositories**: 70+ repositories with comprehensive Sanskrit dictionaries

### **Key Repositories Identified**:

#### **1. csl-orig** ⭐⭐⭐⭐⭐
- **Description**: Data for ALL dictionaries of Cologne (master repository)
- **Format**: Python-based, git workflow
- **Stars**: 18
- **Forks**: 10
- **Status**: Active development

#### **2. MWS (Monier-Williams Sanskrit Dictionary)** ⭐⭐⭐⭐⭐
- **Description**: The most authoritative Sanskrit-English dictionary (Oxford, 1899)
- **Format**: HTML
- **Coverage**: ~180,000 entries
- **Stars**: 9
- **Forks**: 5

#### **3. PWG (Petersburg Wörterbuch)** ⭐⭐⭐⭐
- **Description**: Boehtlingk und Roth Sanskrit Wörterbuch (7 volumes, 1855-1875)
- **Format**: Python
- **Coverage**: Comprehensive Vedic and Classical Sanskrit

#### **4. PWK (Shorter Petersburg Dictionary)** ⭐⭐⭐⭐
- **Description**: Sanskrit-Wörterbuch in kürzerer Fassung (7 volumes, 1879-1889)
- **Format**: HTML
- **Coverage**: Condensed version of PWG

---

## 📚 **Additional Resources Discovered**:

### **5. rahular/itihasa** ⭐⭐⭐⭐
- **Description**: Large-scale Sanskrit-English translation corpus
- **Content**: 93,000 Sanskrit shlokas with English translations
- **Source**: M. N. Dutt's translations
- **Format**: Structured dataset

### **6. buda-base/sanskrit-stemming-data** ⭐⭐⭐
- **Description**: Sanskrit lexicographical and morphological data
- **Content**: Word stems, morphology, grammar rules
- **Use Case**: Linguistic analysis and word formation

### **7. UniversalDependencies/UD_Sanskrit-Vedic** ⭐⭐⭐
- **Description**: Treebank of Vedic Sanskrit
- **Content**: 4,000 sentences, 27,000 words from Ṛgveda
- **Format**: Annotated grammatical structure
- **Use Case**: Syntactic analysis

### **8. sanskrit/data** ⭐⭐⭐
- **Description**: Versioned Sanskrit linguistic data
- **Coverage**: Almost all lexical forms in Classical Sanskrit literature
- **Format**: Structured data from multiple sources

---

## 🎯 **Recommended Import Strategy**:

### **Phase 1: Core Dictionaries** (CRITICAL)
1. **Monier-Williams (MWS)** - 180,000 entries
2. **Petersburg Wörterbuch (PWG)** - Comprehensive Vedic coverage

### **Phase 2: Translation Corpus** (HIGH VALUE)
3. **Itihasa** - 93,000 pre-translated shlokas

### **Phase 3: Morphological Data** (MEDIUM VALUE)
4. **sanskrit-stemming-data** - Word formation rules
5. **UD_Sanskrit-Vedic** - Grammatical structure

---

## 💡 **Impact on Translation Layer Architecture**:

### **Before** (LLM-Dependent):
```
Sanskrit Verse → OpenAI API → English Translation ($$$)
```

### **After** (Internal Knowledge Base):
```
Sanskrit Verse → Internal Dictionary Lookup → English Translation (FREE)
                     ↓ (if not found)
                 OpenAI API (fallback)
```

### **Estimated Cost Savings**:
- **Dictionary coverage**: ~80% of common words
- **LLM fallback**: ~20% of rare/compound words
- **Cost reduction**: 80% savings on translation costs
- **Quality improvement**: Authoritative scholarly translations vs. LLM guesses

---

## 📊 **Database Schema Impact**:

### **New Tables Needed**:

1. **`dictionary_entries`**
   - word (Sanskrit)
   - definition (English)
   - source_dictionary (MWS, PWG, etc.)
   - part_of_speech
   - etymology
   - usage_examples

2. **`word_stems`**
   - root (dhatu)
   - stem_form
   - grammatical_category
   - derivation_rules

3. **`grammatical_rules`**
   - rule_id
   - rule_type (sandhi, samasa, etc.)
   - description
   - examples

4. **`pre_translated_corpus`**
   - sanskrit_text
   - english_translation
   - source (Dutt, etc.)
   - text_reference

---

## ✅ **Feasibility Assessment**:

**Monier-Williams Dictionary Import**:
- **Feasibility**: ✅ HIGHLY FEASIBLE
- **Format**: HTML (easily parseable)
- **Size**: ~180,000 entries (~50-100 MB)
- **Estimated Import Time**: 2-4 hours

**Petersburg Wörterbuch Import**:
- **Feasibility**: ✅ FEASIBLE
- **Format**: Python/HTML
- **Size**: Larger than MW (comprehensive)
- **Estimated Import Time**: 4-6 hours

**Itihasa Translation Corpus**:
- **Feasibility**: ✅ HIGHLY FEASIBLE
- **Format**: Structured dataset
- **Size**: 93,000 shlokas (~20-30 MB)
- **Estimated Import Time**: 1-2 hours

---

## 🚀 **Recommendation**:

**INTEGRATE ALL THREE** into Transformation 2.0:
- Phase 2A: Import Monier-Williams Dictionary (2-4 hours)
- Phase 2B: Import Itihasa Translation Corpus (1-2 hours)
- Phase 2C: Import Petersburg Wörterbuch (4-6 hours)

**Total Additional Time**: 7-12 hours  
**Total ROI**: 80% cost savings + authoritative translations + self-sufficient system

---

## 🎯 **Next Steps**:

1. Update database schema to include linguistic tables
2. Create import scripts for each dictionary
3. Design Linguistics Expert persona to use internal dictionaries FIRST
4. Implement LLM fallback for rare words
5. Create self-improving loop (LLM translations → enrich dictionary)

---

**Status**: Reconnaissance complete, ready to integrate into Transformation 2.0 plan.
