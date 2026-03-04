from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from .models import Category, Transaction
from .forms import CategoryForm, TransactionForm, SignupForm

# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tracker/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        transactions = Transaction.objects.filter(user=user)

        # Calculate totals
        total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        balance = total_income - total_expense

        category_totals = (
            transactions
            .values('category__name', 'type')
            .annotate(total=Sum('amount'))
        )

        category_map = {}
        for item in category_totals:
            category_name = item['category__name']
            if category_name not in category_map:
                category_map[category_name] = {
                    'name': category_name,
                    'income': 0,
                    'expense': 0,
                }

            if item['type'] == 'income':
                category_map[category_name]['income'] = item['total'] or 0
            elif item['type'] == 'expense':
                category_map[category_name]['expense'] = item['total'] or 0

        category_comparison = list(category_map.values())
        category_comparison.sort(key=lambda row: (row['income'] + row['expense']), reverse=True)

        chart_max = 0
        for row in category_comparison:
            row_max = max(row['income'], row['expense'])
            if row_max > chart_max:
                chart_max = row_max

        category_chart_data = [
            {
                'name': row['name'],
                'income': float(row['income']),
                'expense': float(row['expense']),
            }
            for row in category_comparison
        ]

        context['total_income'] = total_income
        context['total_expense'] = total_expense
        context['balance'] = balance
        context['recent_transactions'] = transactions.order_by('-date')[:5]  # Last 5 transactions
        context['category_comparison'] = category_comparison
        context['category_chart_max'] = chart_max
        context['category_chart_data'] = category_chart_data

        return context


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'tracker/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        # Filtering logic can be added here
        return queryset.order_by('-date')


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'tracker/transaction_form.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'tracker/transaction_form.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'tracker/transaction_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'tracker/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tracker/category_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tracker/category_form.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'tracker/category_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
