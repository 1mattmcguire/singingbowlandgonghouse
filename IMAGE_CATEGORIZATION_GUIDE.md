# Image Categorization Guide for "Smiles We Created" Page

## Overview
The "Smiles We Created" page automatically organizes images based on their filenames. Simply add images to the `main/static/main/images/` folder with descriptive names, and they will be automatically placed in the correct sections.

## How It Works

The system scans all images in the `main/static/main/images/` folder and categorizes them based on keywords in their filenames.

## Image Categories

### 1. **School Bags** (Feature Card)
**Keywords to include in filename:**
- `bag`
- `bags`
- `school bag`
- `schoolbag`

**Examples:**
- `new school bags.jpeg` ✅
- `students with bags.jpeg` ✅
- `schoolbag distribution.jpeg` ✅

**Location:** First feature card (School Bags section)

---

### 2. **Stationery Items** (Feature Card)
**Keywords to include in filename:**
- `stationery`
- `stationary`
- `stationeryitem`
- `stationerycopy`

**Examples:**
- `stationery items.jpeg` ✅
- `stationerycopy.jpeg` ✅
- `stationery distribution.jpeg` ✅

**Location:** Second feature card (Stationery Items section)

---

### 3. **School Uniforms** (Feature Card)
**Keywords to include in filename:**
- `uniform`
- `education support`

**Examples:**
- `school uniforms.jpeg` ✅
- `education support.jpeg` ✅
- `students in uniform.jpeg` ✅

**Location:** Third feature card (School Uniforms section)

---

### 4. **Scholarships** (Feature Card)
**Keywords to include in filename:**
- `scholarship`
- `momentofjoeey`
- `momentofjoy`

**Examples:**
- `scholarship recipients.jpeg` ✅
- `momentofjoeey.jpeg` ✅
- `scholarship ceremony.jpeg` ✅

**Location:** Fourth feature card (Scholarships section)

---

### 5. **Gallery** (Impact Gallery Section)
**Keywords to include in filename:**
- `education`
- `moment`
- `student`
- `impact`
- `smile`
- `joy`

**Examples:**
- `Education for all.jpeg` ✅
- `momentofjoy.jpeg` ✅
- `students receiving.jpeg` ✅
- `impact image.jpeg` ✅

**Location:** Gallery grid section (displays all matching images)

---

## Important Notes

### Images Automatically Excluded
The system automatically excludes images that contain these keywords (to avoid mixing with product images):
- `logo`, `gong`, `bowl`, `handpan`, `chakra`, `tamtam`, `nipple`
- `scroll`, `training`, `therapy`, `healing`
- `aboutus`, `hero`, `mainimage`, `bgimg`
- `map`, `whatsapp`, `wechat`, `google`
- Product-related terms: `jam`, `black`, `tiger`, `matt`, `plain`
- Other product terms: `buddhacham`, `kopre`, `thado`, `ulta`, `stand`, `manipuree`

### Multiple Images
- **Feature Cards:** Only the **first image** in each category is displayed in the feature card
- **Gallery:** **All matching images** are displayed in the gallery grid

### Image Priority
1. Images are first checked for feature card categories (School Bags, Stationery, Uniforms, Scholarships)
2. If not matching a feature card category, images with education-related keywords go to the Gallery
3. Images with `student` or `receiving` in the filename are automatically added to Gallery

---

## Quick Reference

| Category | Keywords | Example Filenames |
|----------|----------|-------------------|
| **School Bags** | bag, bags, school bag | `new school bags.jpeg` |
| **Stationery** | stationery, stationary | `stationery items.jpeg` |
| **Uniforms** | uniform, education support | `education support.jpeg` |
| **Scholarships** | scholarship, momentofjoeey | `scholarship ceremony.jpeg` |
| **Gallery** | education, moment, student, impact, smile, joy | `Education for all.jpeg` |

---

## How to Add Images

1. **Name your image file** with descriptive keywords (see above)
2. **Place the image** in `main/static/main/images/` folder
3. **Refresh the page** - images will automatically appear in the correct section!

### Example Workflow:
```
1. Take a photo of students receiving school bags
2. Name it: "students receiving school bags.jpeg"
3. Copy to: main/static/main/images/
4. Refresh the Smiles page
5. Image appears in Gallery section automatically!
```

---

## Troubleshooting

### Image not showing?
- ✅ Check the filename contains the correct keywords
- ✅ Ensure the image is in `main/static/main/images/` folder
- ✅ Check the image extension is `.jpg`, `.jpeg`, `.png`, `.gif`, or `.webp`
- ✅ Make sure the filename doesn't contain excluded keywords (like `gong`, `bowl`, etc.)

### Image in wrong section?
- The system uses the first matching keyword found
- If an image matches multiple categories, it goes to the first matching category
- To change placement, rename the file with different keywords

---

## Current Images Detected

The system will automatically detect and categorize images when you:
1. Add new images to the folder
2. Refresh the page
3. The view function scans the folder on each page load

**No manual configuration needed!** Just name your images correctly and they'll appear in the right place.







