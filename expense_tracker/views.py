from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Transaction, Category


# ==========================
# Transaction Views
# ==========================

@login_required
def transaction_list(request):

    # ==========================
    # Get Filter Values
    # ==========================
    query = request.GET.get(
        "q",
        ""
    )

    transaction_type = request.GET.get(
        "type",
        ""
    )

    category_id = request.GET.get(
        "category",
        ""
    )

    transaction_date = request.GET.get(
        "date",
        ""
    )

    # ==========================
    # Base QuerySet
    # ==========================
    transactions = Transaction.objects.filter(
        user=request.user,
    )

    # ==========================
    # Search
    # ==========================
    if query:

        transactions = transactions.filter(

            Q(title__icontains=query)

            |

            Q(category__name__icontains=query)

            |

            Q(description__icontains=query)

        )

    # ==========================
    # Transaction Type Filter
    # ==========================
    if transaction_type:

        transactions = transactions.filter(
            transaction_type=transaction_type
        )

    # ==========================
    # Category Filter
    # ==========================
    if category_id:

        transactions = transactions.filter(
            category_id=category_id
        )

    # ==========================
    # Date Filter
    # ==========================
    if transaction_date:

        transactions = transactions.filter(
            transaction_date=transaction_date
        )

    # ==========================
    # Sort Transactions
    # ==========================
    transactions = transactions.order_by(
        "-transaction_date",
        "-id",
    )

    # ==========================
    # Pagination
    # ==========================
    paginator = Paginator(
        transactions,
        10,
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    # ==========================
    # Categories for Dropdown
    # ==========================
    categories = Category.objects.filter(
        user=request.user,
    ).order_by(
        "name"
    )

    # ==========================
    # Context
    # ==========================
    context = {

        "page_obj": page_obj,

        "transactions": page_obj,

        "categories": categories,

        "query": query,

        "transaction_type": transaction_type,

        "category_id": category_id,

        "transaction_date": transaction_date,

    }

    return render(

        request,

        "expense_tracker/transaction_list.html",

        context,

    )


@login_required
def add_transaction(request):

    if request.method == "POST":

        Transaction.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            amount=request.POST.get("amount"),
            transaction_type=request.POST.get("transaction_type"),
            category_id=request.POST.get("category"),
            transaction_date=request.POST.get("transaction_date"),
            description=request.POST.get("description"),
        )

        messages.success(
            request,
            "Transaction added successfully.",
        )

        return redirect("transaction_list")

    categories = Category.objects.filter(
        user=request.user,
    )

    return render(
        request,
        "expense_tracker/add_transaction.html",
        {
            "categories": categories,
        },
    )

@login_required
def edit_transaction(request, id):

    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user,
    )

    if request.method == "POST":

        transaction.title = request.POST.get("title")
        transaction.amount = request.POST.get("amount")
        transaction.transaction_type = request.POST.get("transaction_type")
        transaction.category_id = request.POST.get("category")
        transaction.transaction_date = request.POST.get("transaction_date")
        transaction.description = request.POST.get("description")

        transaction.save()

        messages.success(
            request,
            "Transaction updated successfully.",
        )

        return redirect("transaction_list")

    categories = Category.objects.filter(
        user=request.user,
    )

    return render(
        request,
        "expense_tracker/edit_transaction.html",
        {
            "transaction": transaction,
            "categories": categories,
        },
    )


@login_required
def delete_transaction(request, id):

    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user,
    )

    if request.method == "POST":

        transaction.delete()

        messages.success(
            request,
            "Transaction deleted successfully.",
        )

        return redirect("transaction_list")

    return render(
        request,
        "expense_tracker/delete_transaction.html",
        {
            "transaction": transaction,
        },
    )


# ==========================
# Category Views
# ==========================

@login_required
def category_list(request):

    categories = Category.objects.filter(
        user=request.user,
    )

    return render(
        request,
        "expense_tracker/category_list.html",
        {
            "categories": categories,
        },
    )


@login_required
def add_category(request):

    if request.method == "POST":

        name = request.POST.get("name")

        try:

            Category.objects.create(
                user=request.user,
                name=name,
            )

            messages.success(
                request,
                "Category created successfully.",
            )

            return redirect("category_list")

        except IntegrityError:

            messages.error(
                request,
                "You already have a category with this name.",
            )

    return render(
        request,
        "expense_tracker/add_category.html",
    )


@login_required
def edit_category(request, id):

    category = get_object_or_404(
        Category,
        id=id,
        user=request.user,
    )

    if request.method == "POST":

        category.name = request.POST.get("name")

        try:

            category.save()

            messages.success(
                request,
                "Category updated successfully.",
            )

            return redirect("category_list")

        except IntegrityError:

            messages.error(
                request,
                "You already have a category with this name.",
            )

    return render(
        request,
        "expense_tracker/edit_category.html",
        {
            "category": category,
        },
    )


@login_required
def delete_category(request, id):

    category = get_object_or_404(
        Category,
        id=id,
        user=request.user,
    )

    if request.method == "POST":

        category.delete()

        messages.success(
            request,
            "Category deleted successfully.",
        )

        return redirect("category_list")

    return render(
        request,
        "expense_tracker/delete_category.html",
        {
            "category": category,
        },
    )


# ==========================
# Dashboard Views
# ==========================


@login_required
def dashboard(request):
    # ==========================
    # Total Income
    # ==========================
    income_result = Transaction.objects.filter(
        user=request.user,
        transaction_type="Income",
    ).aggregate(
        total=Sum("amount")
    )

    income = income_result["total"]

    if income is None:
        income = 0

    # ==========================
    # Total Expense
    # ==========================
    expense_result = Transaction.objects.filter(
        user=request.user,
        transaction_type="Expense",
    ).aggregate(
        total=Sum("amount")
    )

    expense = expense_result["total"]

    if expense is None:
        expense = 0

    # ==========================
    # Balance
    # ==========================
    balance = income - expense

    # ==========================
    # Recent Transactions
    # ==========================
    recent_transactions = Transaction.objects.filter(
        user=request.user,
    )

    recent_transactions = recent_transactions.order_by(
        "-transaction_date"
    )

    recent_transactions = recent_transactions[:5]

    # ==========================
    # Monthly Income
    # ==========================
    monthly_income = Transaction.objects.filter(
        user=request.user,
        transaction_type="Income",
    )

    monthly_income = monthly_income.annotate(
        month=ExtractMonth("transaction_date")
    )

    monthly_income = monthly_income.values(
        "month"
    )

    monthly_income = monthly_income.annotate(
        total=Sum("amount")
    )

    monthly_income = monthly_income.order_by(
        "month"
    )

    # ==========================
    # Monthly Expense
    # ==========================
    monthly_expense = Transaction.objects.filter(
        user=request.user,
        transaction_type="Expense",
    )

    monthly_expense = monthly_expense.annotate(
        month=ExtractMonth("transaction_date")
    )

    monthly_expense = monthly_expense.values(
        "month"
    )

    monthly_expense = monthly_expense.annotate(
        total=Sum("amount")
    )

    monthly_expense = monthly_expense.order_by(
        "month"
    )

    # ==========================
    # Month Names
    # ==========================
    month_names = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    # ==========================
    # Convert Income QuerySet to Dictionary
    # ==========================
    income_dictionary = {}

    for row in monthly_income:
        income_dictionary[row["month"]] = row["total"]

    # ==========================
    # Convert Expense QuerySet to Dictionary
    # ==========================
    expense_dictionary = {}

    for row in monthly_expense:
        expense_dictionary[row["month"]] = row["total"]

    # ==========================
    # Chart Lists
    # ==========================
    monthly_labels = []

    monthly_income_chart = []

    monthly_expense_chart = []

    # ==========================
    # Build 12 Months
    # ==========================
    for month_number in range(1, 13):

        monthly_labels.append(
            month_names[month_number - 1]
        )

        if month_number in income_dictionary:
            monthly_income_chart.append(
                income_dictionary[month_number]
            )
        else:
            monthly_income_chart.append(0)

        if month_number in expense_dictionary:
            monthly_expense_chart.append(
                expense_dictionary[month_number]
            )
        else:
            monthly_expense_chart.append(0)

    # ==========================
    # Expense by Category
    # ==========================
    expense_by_category = Transaction.objects.filter(
        user=request.user,
        transaction_type="Expense",
    )

    expense_by_category = expense_by_category.values(
        "category__name"
    )

    expense_by_category = expense_by_category.annotate(
        total=Sum("amount")
    )

    expense_by_category = expense_by_category.order_by(
        "category__name"
    )

    # ==========================
    # Pie Chart Lists
    # ==========================
    category_labels = []

    category_totals = []

    # ==========================
    # Build Pie Chart Data
    # ==========================
    for row in expense_by_category:

        category_labels.append(
            row["category__name"]
        )

        category_totals.append(
            float(row["total"])
        )
    

    # ==========================
    # Context
    # ==========================
    context = {
        "income": income,
        "expense": expense,
        "balance": balance,
        "recent_transactions": recent_transactions,
        "monthly_labels": monthly_labels,
        "monthly_income_chart": monthly_income_chart,
        "monthly_expense_chart": monthly_expense_chart,
        "category_labels": category_labels,
        "category_totals": category_totals,
    }

    return render(
        request,
        "expense_tracker/dashboard.html",
        context,
    )